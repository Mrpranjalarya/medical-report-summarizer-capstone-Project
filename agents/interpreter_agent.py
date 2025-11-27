# agents/interpreter_agent.py
"""
InterpreterAgent
Converts extracted parameter facts into:
 - status: low/normal/high/unknown
 - risk: none/low/moderate/high
 - urgency: none/monitor/urgent
 - explanation: human-readable sentence
 - suggested_action: non-prescriptive suggestion (for Recommender)

Input: list of items like:
  [{"name":"cholesterol", "value":165, "unit":"mg/dL", "raw_line":"ldl 165 mg/dL"}]

Output: list of dicts with keys:
  name, value, unit, status, risk, urgency, explanation, suggested_action
"""

from typing import List, Dict, Any, Optional

# Base reference ranges. Expand as needed.
RANGES = {
    "hemoglobin": {"male": (13.5, 17.5), "female": (12.0, 15.5), "all": (12.0, 17.5)},
    "wbc": {"all": (4.0, 11.0)},  # x10^3/µL
    "rbc": {"male": (4.5, 5.9), "female": (4.0, 5.2), "all": (4.0, 5.9)},
    "platelets": {"all": (150, 450)},  # x10^3/µL
    "cholesterol": {"all": (0, 200)},  # mg/dL (total cholesterol; LDL/HDL handled elsewhere)
    "glucose": {"all": (70, 99)},  # fasting mg/dL
    "creatinine": {"all": (0.7, 1.3)}  # mg/dL
}

# Urgency multipliers for extremely abnormal values
URGENT_MULTIPLIER = {
    # if value > high * multiplier => urgent
    "default": 2.0,
    "glucose": 3.0,       # extremely high glucose could be urgent (very approximate)
    "creatinine": 2.5
}

class InterpreterAgent:
    def __init__(self):
        self.agent_name = "InterpreterAgent"

    def _get_ranges(self, name: str, sex: str) -> Optional[tuple]:
        """Return (low, high) for given parameter name and patient sex if available."""
        spec = RANGES.get(name)
        if not spec:
            return None
        # prefer sex-specific, fall back to 'all'
        return spec.get(sex) or spec.get("all")

    def _assess_risk_and_urgency(self, name: str, value: float, low: float, high: float) -> Dict[str, Any]:
        """Return status, risk, urgency, suggested_action based on ranges and heuristics."""
        status = "unknown"
        risk = "none"
        urgency = "none"
        suggested_action = "Monitor and follow up with healthcare provider as needed."

        try:
            if value < low:
                status = "low"
                # degree of abnormality
                pct = (low - value) / (low if low else 1)
                if pct > 0.25:
                    risk = "moderate"
                    suggested_action = "Follow up with clinician; may require further evaluation."
                else:
                    risk = "low"
                    suggested_action = "Repeat test or discuss with clinician if symptomatic."
            elif value > high:
                status = "high"
                # severity measured as proportion above high
                multiplier = value / (high if high else 1)
                # default urgent threshold
                default_mult = URGENT_MULTIPLIER.get(name, URGENT_MULTIPLIER["default"])
                if multiplier >= default_mult:
                    risk = "high"
                    urgency = "urgent"
                    suggested_action = "Seek clinician advice promptly; consider earlier follow-up."
                elif multiplier >= 1.5:
                    risk = "moderate"
                    urgency = "monitor"
                    suggested_action = "Discuss with clinician; consider therapeutic/lifestyle changes."
                else:
                    risk = "low"
                    suggested_action = "Lifestyle modifications and repeat testing as advised."
            else:
                status = "normal"
                risk = "none"
                urgency = "none"
                suggested_action = "Maintain healthy lifestyle; routine monitoring."
        except Exception:
            status = "unknown"
            risk = "unknown"
            urgency = "none"
            suggested_action = "No action suggested due to insufficient data."

        return {
            "status": status,
            "risk": risk,
            "urgency": urgency,
            "suggested_action": suggested_action
        }

    def run(self, extracted: List[Dict[str, Any]], patient_info: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Interpret extracted facts.
        :param extracted: list of dicts from ExtractorAgent (keys: name, value, unit, raw_line, ...)
        :param patient_info: optional dict with 'sex' and 'age' (sex: 'male'|'female'|'all')
        :return: list of interpreted dicts
        """
        sex = "all"
        age = None
        if patient_info:
            sex = patient_info.get("sex", "all") or "all"
            age = patient_info.get("age")

        results: List[Dict[str, Any]] = []

        for item in extracted:
            name = item.get("name")
            value = item.get("value")
            unit = item.get("unit", "")
            raw = item.get("raw_line", "")

            # default output structure
            interpreted = {
                "name": name,
                "value": value,
                "unit": unit,
                "status": "unknown",
                "risk": "unknown",
                "urgency": "none",
                "explanation": "",
                "suggested_action": ""
            }

            if value is None:
                interpreted["status"] = "unknown"
                interpreted["risk"] = "unknown"
                interpreted["explanation"] = f"{name}: mentioned but no numeric value detected in report."
                interpreted["suggested_action"] = "Obtain numeric value (repeat test or check original report)."
                results.append(interpreted)
                continue

            ranges = self._get_ranges(name, sex)
            if not ranges:
                # no configured range
                interpreted["status"] = "unknown"
                interpreted["risk"] = "unknown"
                interpreted["explanation"] = f"{name.title()} = {value}{(' ' + unit) if unit else ''}. No reference range configured."
                interpreted["suggested_action"] = "Provide clinical context (age/sex) or add reference ranges."
                results.append(interpreted)
                continue

            low, high = ranges
            assessment = self._assess_risk_and_urgency(name, value, low, high)

            # build explanation sentence
            explanation = f"{name.title()} = {value}{(' ' + unit) if unit else ''}. Normal range: {low} - {high}."
            if assessment["status"] == "high":
                explanation += f" This value is above the expected range (status: HIGH)."
            elif assessment["status"] == "low":
                explanation += f" This value is below the expected range (status: LOW)."
            else:
                explanation += " This is within the normal range."

            # urgent note
            if assessment["urgency"] == "urgent":
                explanation += " Urgent attention is recommended."

            interpreted.update({
                "status": assessment["status"],
                "risk": assessment["risk"],
                "urgency": assessment["urgency"],
                "explanation": explanation,
                "suggested_action": assessment["suggested_action"]
            })

            # add patient-context note if age/sex available (non-diagnostic)
            if age is not None:
                interpreted["explanation"] += f" (Patient age: {age})."

            # keep original raw line for traceability
            interpreted["raw_line"] = raw

            results.append(interpreted)

        return results
