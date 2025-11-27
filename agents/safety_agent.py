# agents/safety_agent.py

import re

class SafetyAgent:
    """
    Ensures final output does not imply medical diagnosis or prescribe medications.
    It softens diagnostic language and removes medication dosage instructions.
    """

    def __init__(self):
        # Patterns to soften / block
        self.diagnosis_patterns = [
            r"\byou have\b",
            r"\byou are diagnosed with\b",
            r"\bthis indicates\b",
            r"\bsuggests\b",
            r"\bthis confirms\b"
        ]

        # Medication dosage patterns
        self.medication_patterns = [
            r"take\s*\d+\s*mg\b",
            r"take\s*\d+\s*mg.*",     # take 5 mg daily
            r"\b\d+\s*mg\b",          # 10 mg
        ]

        self.disclaimer_text = (
            "\n\n⚠️ **Disclaimer:** This is an educational summary only and "
            "is not a substitute for medical advice, diagnosis, or treatment. "
            "Always consult a licensed healthcare professional."
        )

    def run(self, text: str):
        if not text:
            return ""

        safe = text

        # Soften diagnostic language → does not give direct diagnosis
        for pattern in self.diagnosis_patterns:
            safe = re.sub(pattern, "may be compatible with", safe, flags=re.IGNORECASE)

        # Remove medication dosage instructions
        for pattern in self.medication_patterns:
            safe = re.sub(pattern, "[medication guidance removed for safety]", safe, flags=re.IGNORECASE)

        # Prevent duplicate disclaimer
        if self.disclaimer_text.strip().lower() not in safe.lower():
            safe += self.disclaimer_text

        return safe
