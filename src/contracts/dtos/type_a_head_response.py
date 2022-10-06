from src.contracts.dtos.base_model import BaseModel


class TypeAHeadResponse(BaseModel):
    results: list[str]
