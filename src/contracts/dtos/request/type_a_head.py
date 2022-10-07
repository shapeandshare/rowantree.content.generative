from src.contracts.dtos.base_model import BaseModel
from src.contracts.dtos.parameter.data import DataParameter
from src.contracts.dtos.parameter.filter import FilterParameter
from src.contracts.dtos.parameter.generation import GenerationParameter


class TypeAHeadRequest(BaseModel):
    data: DataParameter
    generation: GenerationParameter
    filter: FilterParameter
