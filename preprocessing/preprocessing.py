import pickle
import pandas as pd
import numpy as np
import json


class Preprocessor:
    def __init__(self, scaler_path: str, encoder_path: str) -> None:
        self.__scaler = pickle.load(open(scaler_path, "rb"))
        self.__encoder = pickle.load(open(encoder_path, "rb"))

    def process_input(self, request_data: str) -> Tuple[Dict, pd.DataFrame]:
        """Scales and encodes POST input for /predict"""
        data = json.loads(request_data)["inputs"]
        data = pd.concat(
            [pd.DataFrame([input], columns=data[0].keys()) for input in data],
            ignore_index=True,
        )
        # Encoding categorical data
        encoded_categorical = pd.DataFrame(self.__encoder.transform(data[["Area"]]).toarray())

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
        ] = self.__scaler.transform(
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
