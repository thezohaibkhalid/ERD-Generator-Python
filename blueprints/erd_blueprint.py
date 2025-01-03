import openai
from flask import request, jsonify
from flask import Blueprint
from Utils.erd_util import ERD_Util
erd_blueprint = Blueprint('erd_blueprint', __name__)

@erd_blueprint.route('/generate_erd', methods=['GET'])
def generate_diagram():
    data = request.json
    requirements = data.get('requirements', '')

    openai.api_key= os.getenv('OPENAI_API_KEY')
    # Call ChatGPT API to generate PlantUML code
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an expert in generating PlantUML code for ERD diagrams."},
            {"role": "user", "content": requirements}
        ]
    )

    erd_util = ERD_Util()

    # Extract PlantUML code from the response
    plantuml_code = response['choices'][0]['message']['content']

    # Encode PlantUML code to create a URL for the PlantUML server
    encoded_uml = erd_util.encode_plantuml(plantuml_code)
    diagram_url = f"https://www.plantuml.com/plantuml/png/{encoded_uml}"

    return jsonify({"diagramUrl": diagram_url})
