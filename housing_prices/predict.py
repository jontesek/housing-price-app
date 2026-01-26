from pathlib import Path

import pandas as pd
import joblib

MODEL_COLUMNS = [
    'longitude', 'latitude', 'housing_median_age', 'total_rooms', 
    'total_bedrooms', 'population', 'households', 'median_income',
    'ocean_proximity_<1H OCEAN', 'ocean_proximity_INLAND', 
    'ocean_proximity_ISLAND', 'ocean_proximity_NEAR BAY', 
    'ocean_proximity_NEAR OCEAN'
]

def get_current_file_dir():
    return Path(__file__).resolve().parent

def load_model(model_name: str):
    root_folder = get_current_file_dir().parent
    file_path = root_folder / "models" / model_name
    return joblib.load(file_path)

def prepare_input_df(item: dict):
    df_single = pd.DataFrame([item])
    df_encoded = pd.get_dummies(df_single)
    return df_encoded.reindex(columns=MODEL_COLUMNS, fill_value=0)

def predict_price(model, df) -> float:
    return model.predict(df)[0]


if __name__ == "__main__":
    input_item = {
        'longitude': -122.64, 'latitude': 38.01, 'housing_median_age': 36.0,
        'total_rooms': 1336.0, 'total_bedrooms': 258.0, 'population': 678.0,
        'households': 249.0, 'median_income': 5.5789, 'ocean_proximity': 'NEAR OCEAN'
    }
    model = load_model("model.joblib")
    input_df = prepare_input_df(input_item)
    price = predict_price(model, input_df)
    print(price)
