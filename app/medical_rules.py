import re

DISCLAIMER = (
    "This is general guidance only. "
    "Please consult a qualified doctor or nurse for proper diagnosis and treatment."
)

SYMPTOM_RULES = {
    "fever": {
        "medicine": "Paracetamol",
        "timing": "After food",
        "advice": "Drink plenty of water and take proper rest."
    },
    "cold": {
        "medicine": "Cetirizine",
        "timing": "After food (preferably at night)",
        "advice": "Avoid cold drinks and dusty environments."
    },
    "cough": {
        "medicine": "Cough syrup (Benadryl type)",
        "timing": "After food",
        "advice": "Warm fluids and steam inhalation can help."
    },
    "headache": {
        "medicine": "Paracetamol",
        "timing": "After food",
        "advice": "Reduce screen time and rest in a quiet, dark room."
    },
    "stomach pain": {
        "medicine": "Antacid (ENO / Gelusil)",
        "timing": "Before food",
        "advice": "Avoid spicy and oily food."
    },
    "vomiting": {
        "medicine": "ORS / Anti-nausea medication",
        "timing": "Small sips frequently",
        "advice": "Stay hydrated and avoid heavy meals."
    }
}


def normalize_input(text: str) -> str:
    """
    Lowercase, remove special characters, normalize spacing.
    """
    text = text.lower()
    text = re.sub(r"[^a-zA-Z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def detect_symptoms(text: str):
    """
    Returns a list of detected symptoms.
    """
    detected = []
    for symptom in SYMPTOM_RULES.keys():
        if symptom in text:
            detected.append(symptom)
    return detected


def apply_rules(symptoms: list):
    """
    Apply rules to all detected symptoms and merge advice.
    """
    results = []
    for symptom in symptoms:
        rule = SYMPTOM_RULES.get(symptom)
        if rule:
            results.append({
                "symptom": symptom,
                "medicine": rule["medicine"],
                "timing": rule["timing"],
                "advice": rule["advice"]
            })
    return results


def build_response(user_input: str):
    clean_text = normalize_input(user_input)
    symptoms = detect_symptoms(clean_text)

    if not symptoms:
        return {
            "confidence": "Low",
            "recommendations": [],
            "message": "Symptoms not clearly recognized.",
            "disclaimer": DISCLAIMER,
            "source": "Rule Engine"
        }

    recommendations = apply_rules(symptoms)

    confidence = "High" if len(recommendations) >= 2 else "Medium"

    return {
    "confidence": confidence,
    "title": "Preliminary Clinical Guidance",
    "summary": "Based on the symptoms you have described, the following general care recommendations are provided for informational purposes only.",
    "recommendations": recommendations,
    "care_note": "If symptoms persist, worsen, or are accompanied by high fever, severe pain, or breathing difficulty, please seek medical attention immediately.",
    "disclaimer": DISCLAIMER,
    "source": "Jyotirmayee Clinic – Digital Health Assistant"
}