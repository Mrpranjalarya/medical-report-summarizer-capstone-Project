# agents/extractor_agent.py

import re
from typing import Dict, Any, List

COMMON_PARAMS = {
    "hemoglobin": ["hemoglobin", "hb"],
    "wbc": ["wbc", "white blood cell", "white blood cells"],
    "rbc": ["rbc", "red blood cell", "red blood cells"],
    "platelets": ["platelet", "platelets"],
    "cholesterol": ["cholesterol", "ldl", "hdl", "triglyceride"],
    "glucose": ["glucose", "blood sugar", "sugar"],
    "creatinine": ["creatinine"],
    "bun": ["bun", "urea"],
    "a1c": ["hba1c", "a1c", "hb1c"],
}

VALUE_RE = re.compile(
    r"([-+]?\d+(?:\.\d+)?)(?:\s*(mg/dl|g/dl|mmol/l|\/µl|x10\^3\/µl|%))?",
    re.I
)

class ExtractorAgent:
    """
    ExtractorAgent — Rule-based medical value extraction agent.
    Purpose:
    - Detect medical measurements from lab reports
    - Extract numerical values and units
    - Output normalized structured data for the next agents

    Output format:
    {
      "agent": "ExtractorAgent",
      "status": "success",
      "facts": [
        {"name": "...", "value": 0.0, "unit": "...", "raw_line": "..."}
      ]
    }
    """

    def __init__(self, debug: bool = False):
        self.debug = debug
        self.agent_name = "ExtractorAgent"

    def log(self, message: str):
        if self.debug:
            print(f"[ExtractorAgent] {message}")

    def run(self, report_text: str) -> Dict[str, Any]:
        if not report_text or not report_text.strip():
            return {
                "agent": self.agent_name,
                "status": "error",
                "error": "Empty report text received",
                "facts": []
            }

        text = report_text.lower()
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

        extracted: List[Dict[str, Any]] = []

        for ln in lines:
            for canonical, keywords in COMMON_PARAMS.items():
                if any(kw in ln for kw in keywords):
                    match = VALUE_RE.search(ln)
                    if match:
                        value = float(match.group(1))
                        unit = match.group(2) or ""
                        extracted.append({
                            "name": canonical,
                            "value": value,
                            "unit": unit,
                            "raw_line": ln
                        })
                        self.log(f"Extracted {canonical} = {value} {unit}")
                    else:
                        # Mention without value
                        extracted.append({
                            "name": canonical,
                            "value": None,
                            "unit": "",
                            "raw_line": ln
                        })
                        self.log(f"Mention detected: {canonical}")
                    break

        # Dedupe
        seen = set()
        dedup = []
        for item in extracted:
            if item["name"] not in seen:
                dedup.append(item)
                seen.add(item["name"])

        return {
            "agent": self.agent_name,
            "status": "success",
            "facts": dedup
        }
