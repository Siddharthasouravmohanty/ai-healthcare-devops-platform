from flask import Blueprint, render_template, request
from medical_rules import build_response

web_routes = Blueprint("web_routes", __name__)

@web_routes.route("/", methods=["GET", "POST"])
def index():
    guidance = None

    if request.method == "POST":
        user_input = request.form.get("symptoms")
        guidance = build_response(user_input)


    return render_template("index.html", guidance=guidance)
