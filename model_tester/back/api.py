from flask import Flask, request, jsonify
from flask_cors import CORS
import util.api_util as utils

app = Flask(__name__)
CORS(app)


@app.route('/load', methods=['POST'])
def load_model():
    if 'model' not in request.form or not request.form['model']:
        utils.load_model()
    else:
        utils.load_model(request.form['model'])
    return "Model Loaded"


@app.route('/list', methods=['GET'])
def list_models():
    return utils.list_models()


@app.route('/recognize', methods=['POST'])
def recognize_mp3():
    if 'audio' not in request.files:
        return 'No file part', 404

    file = request.files['audio']
    return jsonify(utils.recognize_mp3(file=file))


if __name__ == '__main__':
    app.run(debug=True)
