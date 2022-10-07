from src.contracts.dtos.base_model import BaseModel
from src.contracts.dtos.prediction import Prediction


class Predictions(BaseModel):
    result: list[Prediction]
