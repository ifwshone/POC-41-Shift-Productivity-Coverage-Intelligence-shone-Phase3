import os
import uuid
import json
from fastapi import APIRouter
from pydantic import BaseModel

try:
    from google import genai
except ImportError:
    genai = None

from assistant.core.scope_guard import evaluate_scope
from assistant.core.intent_classifier import classify_intent
from assistant.core.output_validator import validate_numeric_fidelity
from assistant.core.query_router import get_priority_items
from assistant.queries.result_queries import get_result_explanation, get_limitations, get_methodology
from assistant.queries.summary_queries import get_data_freshness

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

@router.post("/query")
async def query_assistant(req: QueryRequest):
    try:
        question = req.question

        # 1. Scope Check
        scope = evaluate_scope(question)
        if scope == "UNSAFE":
            intent_str, status, answer, result = "unsafe", "unsafe", "Request blocked by security policy.", {}
        elif scope == "OUT_OF_SCOPE":
            intent_str, status, answer, result = "unsupported", "unsupported", "I can only answer questions about current Shift Productivity rankings.", {}
        else:
            # 2. Intent Classification — returns {"intent": str, "parameters": dict}
            intent_result = classify_intent(question)
            # Always extract the string; guard against legacy string returns too
            if isinstance(intent_result, dict):
                intent_str = intent_result.get("intent", "OUT_OF_SCOPE")
                intent_params = intent_result.get("parameters", {})
            else:
                intent_str = str(intent_result)
                intent_params = {}

            status = "answered"
            result = {}

            if intent_str == "AMBIGUOUS":
                status, answer, result = "unsupported", "Could you clarify which specific facility and team you want to review?", {"limitation": "Assistant requires specific entity names."}
            elif intent_str == "OUT_OF_SCOPE":
                status, answer, result = "unsupported", "I can only answer questions about current Shift Productivity rankings.", {}
            elif intent_str == "explain_method":
                result = get_methodology()
            elif intent_str == "explain_limitation":
                result = get_limitations()
            elif intent_str == "get_data_freshness":
                result = get_data_freshness()
            elif intent_str == "explain_result":
                # Prefer entity from parameters; fall back to question text scan
                entity = intent_params.get("entity_id", "facility_a_night_watch")
                if not entity or "facility_b" in question.lower():
                    entity = "facility_b_night_watch"
                result = get_result_explanation(entity)
            else:
                # Default: list_priority_items
                result = get_priority_items()

            if result.get("status") == "unavailable":
                status, answer = "unavailable", result.get("limitation", "No matching data available.")
            else:
                answer = "Request processed deterministically based on approved data outputs."

        # 3. LLM / Fallback Logic
        llm_status = "unavailable (Missing Config)"
        llm_explanation = None
        api_key = os.environ.get("GEMINI_API_KEY")

        if api_key and genai and status == "answered":
            try:
                client = genai.Client(api_key=api_key)
                response = client.models.generate_content(
                    model=os.environ.get("GEMINI_MODEL", "gemini-2.0-flash-lite"),
                    contents=f"Explain this data naturally: {result.get('answer_data')} Evidence: {result.get('evidence')}"
                )
                if validate_numeric_fidelity(response.text, result):
                    llm_status = "success"
                    llm_explanation = response.text
                else:
                    llm_status = "rejected_by_validator (Hallucination Detected)"
            except Exception as llm_err:
                llm_status = f"unavailable ({type(llm_err).__name__})"

        # Ensure evidence is always a list to prevent React crashes
        ev_list = result.get("evidence")
        if not isinstance(ev_list, list):
            ev_list = []

        # Build a human-readable deterministic_finding from result data
        answer_data = result.get("answer_data", {})
        if answer_data and isinstance(answer_data, dict):
            items = answer_data.get("items", [])
            if items and isinstance(items, list):
                # Priority items: build a readable summary
                lines = []
                for item in items[:3]:
                    if isinstance(item, dict):
                        entity = item.get("entity_id", "").replace("_", " ")
                        rank = item.get("priority_rank", "")
                        val = item.get("result_value", "")
                        cat = item.get("result_category", "")
                        finding = item.get("finding", "")
                        if finding:
                            lines.append(f"#{rank} {entity}: {finding}")
                        else:
                            lines.append(f"#{rank} {entity} — gap {val} ({cat})")
                deterministic_finding = "\n".join(lines) if lines else answer
            else:
                # Methodology / limitations / freshness: build from key fields
                parts = []
                for k, v in answer_data.items():
                    if isinstance(v, str) and v:
                        parts.append(v)
                    elif isinstance(v, list):
                        parts.extend([str(i) for i in v[:5] if isinstance(i, str)])
                deterministic_finding = " ".join(parts) if parts else answer
        else:
            deterministic_finding = answer

        return {
            "answer_id": f"ANS-{uuid.uuid4().hex[:8]}",
            "status": status,
            "intent": intent_str,          # always a plain string now
            "llm_status": llm_status,
            "answer": answer,
            "deterministic_finding": deterministic_finding,
            "llm_explanation": llm_explanation,
            "evidence": ev_list,
            "evidence_references": ev_list,
            "key_values": {},
            "metadata": result.get("metadata") or {
                "data_version": "1.0.0",
                "method_version": "1.0.0",
                "quality_status": "validated"
            },
            "limitation": result.get("limitation") or "Synthetic data only. Not for real staffing decisions.",
            "suggested_follow_ups": [
                "Which group ranks highest?",
                "Which groups are below baseline?",
                "What are the limitations of this data?",
                "When was this data generated?"
            ]
        }

    except Exception as e:
        return {
            "answer_id": f"ANS-{uuid.uuid4().hex[:8]}",
            "status": "error",
            "intent": "error",
            "llm_status": "error",
            "answer": f"Backend Error: {str(e)}",
            "deterministic_finding": "",
            "llm_explanation": None,
            "evidence": [],
            "evidence_references": [],
            "key_values": {},
            "metadata": {
                "data_version": "1.0.0",
                "method_version": "1.0.0",
                "quality_status": "rejected"
            },
            "limitation": "Error processing request.",
            "suggested_follow_ups": []
        }