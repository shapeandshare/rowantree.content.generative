from src.models.base_model import BaseModel
from src.models.prediction import Prediction


class Predictions(BaseModel):
    results: list[Prediction]
