import os

ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
IS_LOCAL = ENVIRONMENT == "local"

MODEL_NAME = os.getenv("MODEL_NAME", "model.joblib")
