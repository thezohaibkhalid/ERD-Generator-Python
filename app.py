from flask import Flask, render_template
from blueprints.erd_blueprint import erd_blueprint
from dotenv import load_dotenv
import os

app = Flask(__name__)
load_dotenv()

# Ensure the Google API key is set
if not os.getenv('GOOGLE_API_KEY'):
    raise ValueError("GOOGLE_API_KEY is not set in the environment variables")

@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

app.register_blueprint(erd_blueprint)

if __name__ == '__main__':
    app.run(debug=True)

