from src.contracts.dtos.base_model import BaseModel


class Prediction(BaseModel):
    generated_text: str
