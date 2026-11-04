def build_evidence_package(intent: str, parameters: dict, answer_data: dict, evidence: list, metadata: dict, limitation: str) -> dict:
    """
    Assembles the exact Grounded Evidence Package contract expected by the LLM.
    Ensures no raw file access is passed to the LLM.
    """
    return {
        "intent": intent,
        "parameters": parameters,
        "answer_data": answer_data,
        "evidence": evidence,
        "metadata": {
            "data_version": metadata.get("data_version"),
            "method_version": metadata.get("method_version"),
            "quality_status": metadata.get("quality_status", "validated")
        },
        "limitation": limitation
    }