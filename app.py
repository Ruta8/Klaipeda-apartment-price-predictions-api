from flask import Flask, request
import json
import pickle
from database.database import connect_to_database, update_database
from preprocessing.preprocessing import process_input

app = Flask(__name__)

model = pickle.load(open("model/model.pkl", "rb"))

@app.route("/predict", methods=["POST"])
def predict() -> str:
    
    features = process_input(request.data)[1]
    input = process_input(request.data)[0]
    print(type(input))
    try:
        prediction = model.predict(features)
        print(type(prediction))
    except:
        return json.dumps({"error": "PREDICTION FAILED"}), 400

    update_database(input, prediction)
    return json.dumps({"Predicted house prices": prediction.tolist()})


@app.route("/history", methods=["GET"])
def show_history() -> str:

    connection = connect_to_database()
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM apartments ORDER BY id DESC LIMIT 10;""")
    prediction_history = cursor.fetchall()
    
    return json.dumps({"Predictions": prediction_history})


if __name__ == "__main__":
    app.run(debug=False)