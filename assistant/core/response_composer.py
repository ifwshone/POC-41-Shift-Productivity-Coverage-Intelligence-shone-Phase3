import uuid
from datetime import datetime, timezone

def compose_response(intent: str, answer: str, evidence_package: dict, status: str = "answered", follow_ups: list = None) -> dict:
    """
    Assembles the final Grounded Response Contract payload.
    """
    key_values = []
    if "answer_data" in evidence_package:
        if isinstance(evidence_package["answer_data"], dict):
            for k, v in evidence_package["answer_data"].items():
                if isinstance(v, (int, float)):
                    key_values.append({"name": k, "value": v})

    return {
        "answer_id": f"ANS-{uuid.uuid4().hex[:8].upper()}",
        "status": status,
        "intent": intent,
        "answer": answer,
        "evidence_references": evidence_package.get("evidence", []),
        "key_values": key_values,
        "metadata": evidence_package.get("metadata", {}),
        "limitation": evidence_package.get("limitation", ""),
        "suggested_follow_ups": follow_ups or ["Which group ranks highest?", "What are the limitations of this data?"]
    }