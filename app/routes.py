from flask import Blueprint, render_template, request
from ai_service import get_ai_guidance

web_routes = Blueprint("web_routes", __name__)

@web_routes.route("/", methods=["GET", "POST"])
def index():
    guidance = None

    if request.method == "POST":
        user_input = request.form.get("symptoms")
        guidance = get_ai_guidance(user_input)

    return render_template("index.html", guidance=guidance)
