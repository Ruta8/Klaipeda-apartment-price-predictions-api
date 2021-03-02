import pickle
import pandas as pd
import numpy as np
import json

scaler = pickle.load(open("model/scaler.pkl", "rb"))
encoder = pickle.load(open("model/encoder.pkl", "rb"))

def process_input(request_data: str) -> np.array:
    """Scales and encodes POST input for /predict"""
    data = json.loads(request_data)["inputs"]
    data = pd.concat(
        [pd.DataFrame([input], columns=data[0].keys()) for input in data],
        ignore_index=True,
    )
    # Encoding categorical data
    encoded_categorical = pd.DataFrame(encoder.transform(data[["Area"]]).toarray())

    # Seperating numerical data from the dataframe and scaling
    numeric_data = data.drop(["Area"], axis=1)
    numeric_data[
        [
            "Room Count",
            "Square Meters",
            "Apartment Floor",
            "Total Floors",
            "Building Age",
        ]
    ] = scaler.transform(
        numeric_data[
            [
                "Room Count",
                "Square Meters",
                "Apartment Floor",
                "Total Floors",
                "Building Age",
            ]
        ]
    )
    # Features for prediction
    features = numeric_data.join(encoded_categorical)
    return data, features