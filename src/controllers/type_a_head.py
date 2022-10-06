from src.controllers.abstract_controller import AbstractController
from src.models.generation_parameters import GenerationParameters
from src.models.type_a_head_request import TypeAHeadRequest
from src.models.type_a_head_response import TypeAHeadResponse
from src.services.text import TextService


class TypeAHeadController(AbstractController):
    text_service: TextService

    def execute(self, request: TypeAHeadRequest) -> TypeAHeadResponse:
        params = GenerationParameters.parse_obj(request.dict(by_alias=True))
        return TypeAHeadResponse(results=self.text_service.execute(prompt=request.text, params=params))
