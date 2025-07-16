import joblib
import pandas as pd

# Load model only once
with open('model.pkl', 'rb') as f:
    model = joblib.load(f)

def predict_premium(features_df: pd.DataFrame):
    return model.predict(features_df)[0]
