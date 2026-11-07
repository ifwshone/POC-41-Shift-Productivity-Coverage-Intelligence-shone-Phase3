import re
import json

NUM = re.compile(r'\b\d+(?:\.\d+)?\b')


def _allowed_numbers(package: dict) -> set:
    """Numbers permitted in an LLM answer: only those present in the approved
    evidence package (values, ranks, versions). No hard-coded allowances."""
    allowed = set(NUM.findall(json.dumps(package)))
    # normalise 40 vs 40.0 so formatting differences are not rejected
    for n in list(allowed):
        f = float(n)
        allowed.add(str(f))
        if f == int(f):
            allowed.add(str(int(f)))
    return allowed


def _check(text: str, package: dict) -> bool:
    if not text:
        return False
    bad = set(NUM.findall(text)) - _allowed_numbers(package)
    if bad:
        print(f"[validator] rejected, numbers not in evidence: {sorted(bad)}")
        return False
    return True


def validate_numeric_fidelity(text: str, result_data: dict) -> bool:
    return _check(text, result_data)


def validate_grounded_response(text: str, evidence_package: dict) -> bool:
    return _check(text, evidence_package)
