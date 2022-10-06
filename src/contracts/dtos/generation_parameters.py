from src.contracts.dtos.base_model import BaseModel


class GenerationParameters(BaseModel):
    epochs: int = 5
    max_length: int = 10
    num_responses: int = 5
    quantile: float = 0.3
