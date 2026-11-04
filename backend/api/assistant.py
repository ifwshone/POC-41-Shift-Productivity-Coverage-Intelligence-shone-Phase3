import os
from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
from google import genai

from assistant.core.scope_guard import evaluate_scope
from assistant.core.intent_classifier import classify_intent
from assistant.core.parameter_validator import validate_parameters
from assistant.core.response_composer import compose_response
from assistant.core.query_router import get_priority_items
from assistant.queries.result_queries import get_result_explanation, get_limitations
from assistant.queries.summary_queries import get_data_freshness
from assistant.core.output_validator import validate_grounded_response

router = APIRouter()

class QueryRequest(BaseModel):
    question: str

class GroundedResponse(BaseModel):
    answer_id: str
    status: str
    intent: Optional[str] = None
    answer: str
    deterministic_finding: str = ""
    llm_explanation: str = ""
    llm_status: str = "unavailable"
    evidence_references: List[dict] = []
    key_values: List[dict] = []
    metadata: Optional[dict] = None
    limitation: Optional[str] = None
    suggested_follow_ups: List[str] = []

@router.post("/query", response_model=GroundedResponse)
async def query_assistant(req: QueryRequest):
    if evaluate_scope(req.question) == "UNSAFE":
        return compose_response("unsafe", "Request blocked by security policy.", {}, "unsafe")

    classification = classify_intent(req.question)
    intent = classification["intent"]
    
    if intent == "OUT_OF_SCOPE":
        return compose_response("unsupported", "I can only answer questions about current Shift Productivity rankings and limitations.", {}, "unsupported")

    try:
        params = validate_parameters(intent, classification.get("parameters", {}))
    except ValueError as e:
        return compose_response(intent, str(e), {}, "unsupported")

    if intent == "list_priority_items":
        data = get_priority_items(limit=params.get("limit", 3), result_category=params.get("result_category", "low"))
    elif intent == "explain_result":
        data = get_result_explanation(params["entity_id"])
    elif intent == "explain_limitation":
        data = get_limitations()
    elif intent == "get_data_freshness":
        data = get_data_freshness()
    else:
        data = {"status": "unavailable", "limitation": "No matching data."}

    if data.get("status") == "unavailable":
        return compose_response(intent, "No matching data available.", data, "unavailable")

    # Extract Deterministic Base
    deterministic_finding = data.get('answer_data', {}).get('finding', 'Valid data retrieved.')
    if intent == "list_priority_items":
        items = data.get('answer_data', {}).get('items', [])
        deterministic_finding = " ".join([i.get("finding", "") for i in items])
        
    api_key = os.getenv("GEMINI_API_KEY")
    model_name = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")
    llm_explanation = ""
    llm_status = "unavailable (Missing Config)"

    if api_key:
        try:
            client = genai.Client(api_key=api_key)
            prompt_template = Path("assistant/prompts/grounded_explanation_prompt.txt").read_text(encoding="utf-8")
            prompt = f"{prompt_template}\n\nQuestion: {req.question}\nEvidence: {data['evidence']}\nLimitation: {data.get('limitation')}\nDeterministic Finding: {deterministic_finding}"
            
            response = client.models.generate_content(
                model=model_name,
                contents=prompt
            )
            raw_llm = response.text.strip()
            
            if validate_grounded_response(raw_llm, data):
                llm_explanation = raw_llm
                llm_status = "success"
            else:
                llm_status = "rejected_by_validator (Hallucination Detected)"
        except Exception as e:
            llm_status = "error (Provider or Network Failure)"

    return compose_response(
        intent=intent,
        answer="Request processed.",
        evidence_package=data,
        status="answered",
        deterministic_finding=deterministic_finding,
        llm_explanation=llm_explanation,
        llm_status=llm_status
    )