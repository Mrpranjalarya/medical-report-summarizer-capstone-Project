# agents/recommender_agent.py

RECOMMENDATIONS = {
    "hemoglobin": {
        "low": ["Increase dietary iron (spinach, legumes), get clinician advice on iron supplementation."],
        "high": ["High hemoglobin can be investigated by clinician; stay hydrated."]
    },
    "cholesterol": {
        "high": ["Reduce saturated fats, increase fiber, consider follow-up lipid panel and clinician consult."],
        "low": []
    },
    "glucose": {
        "high": ["Reduce simple carbs, schedule fasting blood glucose test, consult clinician for diabetes screening."]
    }
}

class RecommenderAgent:
    def __init__(self):
        pass

    def run(self, interpreted):
        recs = []
        for it in interpreted:
            name = it.get("name")
            status = it.get("status")
            if not name or not status:
                continue
            rules = RECOMMENDATIONS.get(name, {})
            rec = rules.get(status, [])
            recs.extend(rec)
        # Default general advice
        if not recs:
            recs.append("Maintain a balanced diet, regular exercise, and follow-up with your healthcare provider.")
        return recs
