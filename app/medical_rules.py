def get_medical_recommendation(symptoms: str):
    symptoms = symptoms.lower()

    rules = {
        "fever": {
            "medicine": "Paracetamol",
            "timing": "After food",
            "advice": "Drink  plenty of water and take rest"
        },
        "cold": {
            "medicine": "AZETHROMICINE",
            "timing": "After food (preferably night)",
            "advice": "Avoid cold drinks and dust exposure"
        },
        "cough": {
            "medicine": "Cough syrup (Benadryl type)",
            "timing": "After food",
            "advice": "Warm fluids help reduce irritation"
        },
        "headache": {
            "medicine": "Paracetamol",
            "timing": "After food",
            "advice": "Avoid screen time and take proper rest"
        },
        "stomach pain": {
            "medicine": "Antacid (ENO / Gelusil)",
            "timing": "Before food",
            "advice": "Avoid spicy and oily food"
        }
    }

    for key, value in rules.items():
        if key in symptoms:
            return {
                "medicine": value["medicine"],
                "timing": value["timing"],
                "advice": value["advice"],
                "source": "Rule-based"
            }

    return {
        "medicine": "Consult a doctor",
        "timing": "N/A",
        "advice": "Symptoms not recognized clearly",
        "source": "Rule-based"
    }
