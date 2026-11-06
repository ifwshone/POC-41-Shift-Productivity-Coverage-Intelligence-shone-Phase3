import json
from pathlib import Path

INTENTS_PATH = Path("assistant/config/supported_intents.json")

def load_supported_intents():
    return json.loads(INTENTS_PATH.read_text(encoding="utf-8"))

def classify_intent(question: str) -> dict:
    """
    Rule-based intent classifier to map natural language to exact bounds.
    Fails safely to OUT_OF_SCOPE if no match is found.
    """
    question_lower = question.lower()
    
    if any(kw in question_lower for kw in ["limitation", "limitations", "weak", "bias"]):
        return {"intent": "explain_limitation", "parameters": {}}
        
    if any(kw in question_lower for kw in ["method", "calculated", "baseline", "how was"]):
        return {"intent": "explain_method", "parameters": {}}
        
    if any(kw in question_lower for kw in ["freshness", "generated", "version", "date", "when"]):
        return {"intent": "get_data_freshness", "parameters": {}}
        
    if any(kw in question_lower for kw in ["why is", "explain", "detail"]):
        entity = None
        for fac in ["facility_a", "facility_b"]:
            for team in ["morning_crew", "evening_crew", "night_watch"]:
                # Check for either the exact ID or the natural language version
                if f"{fac}_{team}" in question_lower or (fac in question_lower and team.replace("_", " ") in question_lower):
                    entity = f"{fac}_{team}"
        
        if entity:
            return {"intent": "explain_result", "parameters": {"entity_id": entity}}
        return {"intent": "AMBIGUOUS", "parameters": {}}

    if any(kw in question_lower for kw in ["rank", "highest", "lowest", "priority", "worst", "best"]):
        # Fix: 'highest priority' or 'highest for review' targets worst performers (low category)
        if "highest for review" in question_lower or "highest priority" in question_lower:
            cat = "low"
        elif any(k in question_lower for k in ["best", "highest", "above"]):
            cat = "high"
        else:
            cat = "low"
        return {"intent": "list_priority_items", "parameters": {"limit": 3, "result_category": cat}}

    return {"intent": "OUT_OF_SCOPE", "parameters": {}}