import os
import google.generativeai as genai
from flask import request, jsonify, Blueprint
from Utils.erd_util import ERD_Util

erd_blueprint = Blueprint('erd_blueprint', __name__)

@erd_blueprint.route('/generate_erd', methods=['POST'])
def generate_diagram():
    data = request.get_json()
    requirements = data.get('requirements', '')
    if not requirements:
        return jsonify({"error": "Requirements are missing"}), 400
    
    api_key = os.getenv('GOOGLE_API_KEY')
    if not api_key:
        return jsonify({"error": "Google API key is missing"}), 500

    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-pro")

    try:
        prompt = f"""You are an expert in generating PlantUML code for ERD diagrams. 
        Generate a PlantUML ERD diagram based on these requirements: {requirements}. 
        Respond ONLY with valid PlantUML code for ERD diagrams, without any explanations or additional text.
        Start the code with @startuml and end with @enduml."""

        response = model.generate_content(prompt)
        plantuml_code = response.text.strip()

        # Validate PlantUML code
        if not plantuml_code.startswith("@startuml") or not plantuml_code.endswith("@enduml"):
            return jsonify({"error": "Invalid PlantUML code generated"}), 500

        erd_util = ERD_Util()

        # Encode PlantUML code to create a URL for the PlantUML server
        encoded_uml = erd_util.encode_plantuml(plantuml_code)
        diagram_url = f"https://www.plantuml.com/plantuml/png/{encoded_uml}"

        return jsonify({"diagramUrl": diagram_url, "plantumlCode": plantuml_code})

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

