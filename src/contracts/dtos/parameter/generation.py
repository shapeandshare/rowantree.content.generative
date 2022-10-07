import secrets
import sys

from src.contracts.dtos.base_model import BaseModel


class GenerationParameter(BaseModel):
    epochs: int = 5
    max_length: int = 10
    num_responses: int = 5
    seed: int = secrets.randbelow(sys.maxsize)
