from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import pickle

data = pd.read_csv("data/cleaned_data.csv")

# Encoding categorical data
encoder = OneHotEncoder().fit(data[["area"]])
encoded_categorical = pd.DataFrame(encoder.transform(data[['area']]).toarray())

# Seperating numerical data from the dataframe
numeric_data = data.drop(["price", "area"], axis=1)

# Scaling numeric data
scaler = StandardScaler()

numeric_data[
    ["room_count", "sq_meters", "apartment_floor", "total_floors", "building_age"]
] = scaler.fit_transform(
    numeric_data[
        ["room_count", "sq_meters", "apartment_floor", "total_floors", "building_age"]
    ]
)

# Joining scaled and encoded features in one dataframe
features = numeric_data.join(encoded_categorical)

X_train, X_test, y_train, y_test = train_test_split(features, data.price)

# Prediction with gradient boosted tree
clf = GradientBoostingRegressor()
clf.fit(X_train, y_train)

with open("model/model.pkl", "wb") as m_file:
    pickle.dump(clf, m_file)

with open("model/scaler.pkl", "wb") as s_file:
    pickle.dump(scaler, s_file)

with open("model/encoder.pkl", "wb") as e_file:
    pickle.dump(encoder, e_file)