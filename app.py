
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Bienvenue sur le site de Beton Brutal !!!'

@app.route('/upload_height/', methods=['POST'])
def upload():
    data = request.data
    data_j = json.loads(data)
    print(data_j)
    return "Hauteur uploadée pour " + data_j["user"]

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)