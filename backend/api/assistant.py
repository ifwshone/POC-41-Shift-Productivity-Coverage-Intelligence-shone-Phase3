import os
from pathlib import Path
from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional
import google.generativeai as genai

from assistant.core.scope_guard import evaluate_scope
from assistant.core.intent_classifier import classify_intent
from assistant.core.parameter_validator import validate_parameters
from assistant.core.response_composer import compose_response
from assistant.core.query_router import get_priority_items
from assistant.queries.result_queries import get_result_explanation, get_limitations
from assistant.queries.summary_queries import get_data_freshness

router = APIRouter()
genai.configure(api_key=os.getenv("GEMINI_API_KEY", ""))

class QueryRequest(BaseModel):
    question: str

class GroundedResponse(BaseModel):
    answer_id: str
    status: str
    intent: Optional[str] = None
    answer: str
    evidence_references: List[dict] = []
    key_values: List[dict] = []
    metadata: Optional[dict] = None
    limitation: Optional[str] = None
    suggested_follow_ups: List[str] = []

@router.post("/query", response_model=GroundedResponse)
async def query_assistant(req: QueryRequest):
    if evaluate_scope(req.question) == "UNSAFE":
        return compose_response("unsafe", "Request blocked by security policy.", {}, "unsafe", [])

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

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        prompt_template = Path("assistant/prompts/grounded_explanation_prompt.txt").read_text(encoding="utf-8")
        prompt = f"{prompt_template}\n\nQuestion: {req.question}\nEvidence: {data['evidence']}\nLimitation: {data.get('limitation')}"
        answer_text = model.generate_content(prompt).text.strip()
    except Exception:
        fallback = data.get('answer_data', {}).get('finding', 'Data retrieved successfully but the LLM is unreachable.')
        answer_text = f"Based on the evidence: {fallback}"

    return compose_response(intent, answer_text, data, "answered")