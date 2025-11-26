# agents/safety_agent.py

class SafetyAgent:
    """
    Simple safety validator:
    - removes direct diagnosis phrases like 'you have X' -> 'findings compatible with X' or advises to consult
    - strips medication dosing
    """
    def __init__(self):
        # Example patterns to block or rephrase could be added
        self.forbidden_phrases = ["you have", "you are diagnosed with", "take 5mg", "take 10 mg"]

    def run(self, text: str):
        if not text:
            return ""
        sane = text
        for fp in self.forbidden_phrases:
            if fp in sane.lower():
                # simple rephrase
                sane = sane.replace(fp, "[REDACTED FOR SAFETY]")
        # Ensure a safety disclaimer appended
        disclaimer = "\n\nDisclaimer: This is an educational summary and not a medical diagnosis. Consult a clinician."
        return sane + disclaimer
