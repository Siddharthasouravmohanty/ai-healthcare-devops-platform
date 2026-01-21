import os
from openai import OpenAI

def get_ai_guidance(symptoms: str, rule_output: dict):
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        return "AI service is not configured. Please contact the system administrator."

    try:
        client = OpenAI(api_key=api_key)

        system_prompt = (
            "You are a professional nursing assistant for a digital health platform. "
            "Provide general health education and care guidance only. "
            "Do not diagnose diseases. Do not provide medication dosages. "
            "Always recommend consulting a healthcare professional for serious or worsening symptoms."
        )

        user_prompt = f"""
Patient symptoms: {symptoms}

Clinical recommendations:
{rule_output}

Please provide:
- A simple explanation of what these symptoms usually indicate
- General self-care advice
- Clear signs of when to seek medical help

Keep the response under 100 words.
"""

        response = client.responses.create(
            model="gpt-4.1-mini",
            input=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=0.3
        )

        return response.output_text

    except Exception as e:
        print("OpenAI Error:", str(e))
        return "AI service is temporarily unavailable. Please follow the clinical guidance above and consult a healthcare professional if needed."
