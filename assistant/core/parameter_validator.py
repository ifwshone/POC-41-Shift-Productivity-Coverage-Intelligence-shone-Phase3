import json
from pathlib import Path

CATALOG_PATH = Path("assistant/config/query_catalog.json")

def load_catalog():
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))

def validate_parameters(intent: str, parameters: dict) -> dict:
    """
    Validates extracted parameters against the query catalog.
    Returns sanitized parameters or raises ValueError.
    """
    catalog = load_catalog()
    if intent not in catalog:
        raise ValueError(f"Unknown intent: {intent}")
        
    rules = catalog[intent]["allowed_parameters"]
    validated = {}
    
    for param_name, rule in rules.items():
        val = parameters.get(param_name, rule.get("default"))
        
        if rule.get("required") and val is None:
            raise ValueError(f"MISSING_PARAMETER: {param_name}")
            
        if val is not None:
            if rule["type"] == "integer":
                try:
                    val = int(val)
                    if "minimum" in rule and val < rule["minimum"]: val = rule["minimum"]
                    if "maximum" in rule and val > rule["maximum"]: val = rule["maximum"]
                except ValueError:
                    raise ValueError(f"Invalid type for {param_name}")
            elif rule["type"] == "string":
                val = str(val)
                if "allowed_values" in rule and val not in rule["allowed_values"]:
                    raise ValueError(f"Invalid value for {param_name}")
                    
        validated[param_name] = val
        
    return validated