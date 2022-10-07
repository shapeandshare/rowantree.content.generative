from src.contracts.dtos.base_model import BaseModel
from src.contracts.filter_type import FilterType


class FilterParameter(BaseModel):
    quantile: float = 0.3
    filters: list[FilterType] = [FilterType.UPPER, FilterType.NUMERIC, FilterType.PUNCTUATION, FilterType.NEWLINE]
