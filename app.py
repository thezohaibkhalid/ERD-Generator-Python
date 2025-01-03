from flask import Flask, request, jsonify, render_template
from blueprints.erd_blueprint import erd_blueprint
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
@app.route('/', methods=['GET'])
def home():
    render_template('index.html')

app.register_blueprint(erd_blueprint)

if __name__ == '__main__':
    app.run(debug=True)

    #Initialized everything and all files added all basic generatioin code