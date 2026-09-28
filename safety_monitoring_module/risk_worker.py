import sys
import warnings
import joblib
import pandas as pd
from pathlib import Path

warnings.filterwarnings("ignore")

BASE = Path(__file__).resolve().parent

MODEL_PATH = BASE / "models" / "safety_risk_model.pkl"
FEATURES_PATH = BASE / "models" / "safety_risk_features.pkl"

model = joblib.load(MODEL_PATH)
features = joblib.load(FEATURES_PATH)


def predict_risk(helmet, vest, gloves, safety_shoes, accident=0):

    data = pd.DataFrame([{
        "Helmet": helmet,
        "Vest": vest,
        "Gloves": gloves,
        "Safety_Shoes": safety_shoes,
        "Accident": accident
    }])

    data = data[features]

    prediction = model.predict(data)[0]

    return prediction


if __name__ == "__main__":

    helmet, vest, gloves, safety_shoes, accident = map(int, sys.argv[1:6])

    result = predict_risk(
        helmet,
        vest,
        gloves,
        safety_shoes,
        accident
    )

    print(result)