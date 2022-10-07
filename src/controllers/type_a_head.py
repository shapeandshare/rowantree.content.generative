from src.contracts.dtos.request.type_a_head import TypeAHeadRequest
from src.contracts.dtos.response.type_a_head import TypeAHeadResponse
from src.controllers.abstract_controller import AbstractController
from src.services.text import TextService


class TypeAHeadController(AbstractController):
    text_service: TextService

    def execute(self, request: TypeAHeadRequest) -> TypeAHeadResponse:
        return TypeAHeadResponse(result=self.text_service.execute(request=request))
