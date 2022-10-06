from src.contracts.dtos.base_model import BaseModel


class Event(BaseModel):
    title: str
    text: str
