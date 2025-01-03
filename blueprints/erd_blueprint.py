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

    # Configure the Google Generative AI API with the API key
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-pro")

    try:
        # Define the prompt to generate PlantUML code based on the provided requirements
        prompt = f"""
        You are an expert in generating accurate PlantUML code for Entity-Relationship Diagrams (ERD) using Chen's ERD notation.
        Based on the provided requirements, generate a valid PlantUML ERD diagram enclosed within the @startuml and @enduml tags.

        Follow these precise guidelines:

        1. **Entities** should be represented in this format:
        `entity ENTITY_NAME {{ attribute1 <<key>> attribute2 }}`
        - `ENTITY_NAME` is the name of the entity.
        - `attribute1` and `attribute2` are actual attributes of the entity. 
        - The primary key attribute should be indicated with `<<key>>`.

        2. **Relationships** should be written as:
        `entity1 -- relationshipName -- entity2`
        - Use `--` to represent a relationship between two entities.
        - The relationship name can be a description or left empty, and cardinality will be indicated separately.
        
        3. **Cardinality** should be indicated as:
        - `entity1 --1-- entity2` for one-to-one relationships.
        - `entity1 --1-- N entity2` for one-to-many relationships.
        - `entity1 --N-- N entity2` for many-to-many relationships.
        
        4. Ensure that the diagram begins with the `@startuml` tag and ends with the `@enduml` tag, with no extra explanations or text.

        Provide **only valid PlantUML code** for the ERD based on the following requirements:

        {requirements}
        """




        # Generate the content using the AI model
        response = model.generate_content(prompt)
        plantuml_code = response.text.strip()

        # Validate the PlantUML code
        if not plantuml_code.startswith("@startchen") or not plantuml_code.endswith("@endchen"):
            return jsonify({"error": "Invalid PlantUML code generated"}), 500

        # Instantiate ERD_Util to encode the PlantUML code
        erd_util = ERD_Util()

        # Encode the PlantUML code to create a URL for the PlantUML server
        encoded_uml = erd_util.encode_plantuml(plantuml_code)

        # Create the URL for the diagram
        diagram_url = f"https://www.plantuml.com/plantuml/png/{encoded_uml}"

        # Return the diagram URL and the original PlantUML code
        return jsonify({"diagramUrl": diagram_url, "plantumlCode": plantuml_code})

    except Exception as e:
        # Return error response if any exception occurs
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500
