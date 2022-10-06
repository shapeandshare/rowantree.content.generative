from src.models.base_model import BaseModel


class TypeAHeadResponse(BaseModel):
    results: list[str]
