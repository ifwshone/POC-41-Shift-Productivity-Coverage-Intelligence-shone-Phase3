import json
from pathlib import Path

POLICY_PATH = Path("assistant/config/assistant_policy.json")

def load_policy():
    return json.loads(POLICY_PATH.read_text(encoding="utf-8"))

def evaluate_scope(question: str) -> str:
    if not question or len(question) > 500:
        return "OUT_OF_SCOPE"
        
    policy = load_policy()
    question_lower = question.lower()
    
    for term in policy["security"]["blocked_terms"]:
        if term in question_lower:
            return "UNSAFE"
            
    # Simple keyword-based intent router for demonstration
    supported_keywords = ["rank", "highest", "lowest", "priority", "why", "limitation", "calculate", "method", "generated"]
    if not any(kw in question_lower for kw in supported_keywords):
        return "OUT_OF_SCOPE"
        
    return "SUPPORTED"
