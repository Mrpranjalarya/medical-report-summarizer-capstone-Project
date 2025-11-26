# agents/interpreter_agent.py

# Simple normal ranges (example). You can expand these.
RANGES = {
    "hemoglobin": {"male": (13.5, 17.5), "female": (12.0, 15.5), "all": (12.0, 17.5)},
    "wbc": {"all": (4.0, 11.0)},  # x10^3/µL
    "rbc": {"male": (4.5, 5.9), "female": (4.0, 5.2), "all": (4.0, 5.9)},
    "platelets": {"all": (150, 450)},  # x10^3/µL
    "cholesterol": {"all": (0, 200)},  # mg/dL
    "glucose": {"all": (70, 99)},  # fasting mg/dL
    "creatinine": {"all": (0.7, 1.3)}
}

class InterpreterAgent:
    """
    Interpret extracted parameters into status + explanation.
    Methods:
      - run(extracted_list, sex="all") -> list of dicts with name,value,status,explanation
    """
    def __init__(self):
        pass

    def run(self, extracted, sex="all"):
        out = []
        for item in extracted:
            name = item.get("name")
            value = item.get("value")
            if value is None:
                out.append({
                    "name": name,
                    "value": None,
                    "status": "unknown",
                    "explanation": f"{name} mentioned but no numeric value detected."
                })
                continue

            ranges = RANGES.get(name, {}).get(sex) or RANGES.get(name, {}).get("all")
            if ranges:
                low, high = ranges
                if value < low:
                    status = "low"
                    explanation = f"{name.title()} is low ({value}). Normal range: {low}-{high}."
                elif value > high:
                    status = "high"
                    explanation = f"{name.title()} is high ({value}). Normal range: {low}-{high}."
                else:
                    status = "normal"
                    explanation = f"{name.title()} is within normal limits ({value})."
            else:
                status = "unknown"
                explanation = f"No reference range configured for {name}."

            out.append({"name": name, "value": value, "status": status, "explanation": explanation})
        return out
