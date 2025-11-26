
# agents/extractor_agent.py
import re

# A minimal list of common lab param names to look for in text
COMMON_PARAMS = {
    "hemoglobin": ["hemoglobin", "hb"],
    "wbc": ["wbc", "white blood cell", "white blood cells"],
    "rbc": ["rbc", "red blood cell", "red blood cells"],
    "platelets": ["platelet", "platelets"],
    "cholesterol": ["cholesterol", "ldl", "hdl", "triglyceride"],
    "glucose": ["glucose", "blood sugar", "sugar"],
    "creatinine": ["creatinine"],
    "bun": ["bun", "urea"],
    "a1c": ["hba1c", "a1c"]
}

# heuristics to find numeric value and unit near the parameter name
VALUE_RE = re.compile(r"([-+]?\d+(?:\.\d+)?)(?:\s*(mg/dL|g/dL|x10\^3/µL|x10\^3/µL|/µL|mmol/L)?)", re.I)

class ExtractorAgent:
    """
    Offline rule-based extractor.
    Methods:
      - run(report_text) -> dict with "extracted": list of param dicts
    """
    def __init__(self):
        pass

    def run(self, report_text: str):
        text = report_text.lower()
        extracted = []

        # find lines with numbers
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]

        for ln in lines:
            for canonical, keywords in COMMON_PARAMS.items():
                for kw in keywords:
                    if kw in ln:
                        # try to find numeric value in same line
                        m = VALUE_RE.search(ln)
                        if m:
                            val = float(m.group(1))
                            unit = m.group(2) or ""
                            extracted.append({
                                "name": canonical,
                                "raw_line": ln,
                                "value": val,
                                "unit": unit,
                                "reference_range": ""
                            })
                        else:
                            # if no numeric value, append mention only
                            extracted.append({
                                "name": canonical,
                                "raw_line": ln,
                                "value": None,
                                "unit": "",
                                "reference_range": ""
                            })
                        break

        # simple dedup by name (keep first occurrence)
        seen = set()
        dedup = []
        for e in extracted:
            if e["name"] not in seen:
                dedup.append(e)
                seen.add(e["name"])

        return {"extracted": dedup}
