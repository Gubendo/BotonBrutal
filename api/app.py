
from flask import Flask, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Bienvenue sur le site de Beton Brutal !!!'

@app.route('/upload_height/', methods=['POST'])
def upload():
    
    data = request.data
    data_j = json.loads(data)
    user = data_j["user"]
    height = data_j["height"]

    df = pd.read_csv("data.csv")
    for index, row in df.iterrows():
        if row["player"] == user:
            print(row)
            current_height = row["current_height"]
            max_height = row["max_height"]
            user_index = index

    df.loc[user_index, "current_height"] = height
    if height > max_height:
        df.loc[user_index, "max_height"] = height
        df.to_csv("data.csv", index=False)
        return "Nouveau record pour " + user + " : " + str(height) + " mètres"
    
    if height < current_height - 50:
        df.to_csv("data.csv", index=False)
        return "Chute terrible de " + str(current_height - height) + " mètres pour " + user
    
    
    df.to_csv("data.csv", index=False)
    return "Hauteur uploadée pour " + user + " : " + str(height) + " mètres"


@app.route('/get_height/')
def get_height():
    df = pd.read_csv("data.csv")
    df_list = df.values.tolist()
    return jsonify(df_list)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=False, threaded=True)