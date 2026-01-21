from flask import Blueprint, render_template, request
from ai_service import get_ai_guidance
from medical_rules import build_response


web_routes = Blueprint("web_routes", __name__)

@web_routes.route("/", methods=["GET", "POST"])
def index():
    guidance = None

    if request.method == "POST":
        user_input = request.form.get("symptoms", "").strip()

        if user_input:
            guidance = build_response(user_input)
            ai_text = get_ai_guidance(user_input, guidance)
            guidance["ai_explanation"] = ai_text
        else:
            guidance = {
                "title": "Input Required",
                "confidence": "N/A",
                "summary": "Please enter your symptoms to receive clinical guidance.",
                "recommendations": [],
                "care_note": "",
                "disclaimer": "No medical advice was generated because no symptoms were provided.",
                "source": "Jyotirmayee Clinic – Digital Health Assistant",
                "ai_explanation": ""
            }

    return render_template("index.html", guidance=guidance)
