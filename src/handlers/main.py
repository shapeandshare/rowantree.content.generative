"""
uvicorn src.handlers.main:app --reload --port 8001 --env-file env/.env.local
"""

import logging

from fastapi import FastAPI
from starlette import status
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from src.contracts.dtos.type_a_head_request import TypeAHeadRequest
from src.contracts.dtos.type_a_head_response import TypeAHeadResponse
from src.controllers.type_a_head import TypeAHeadController
from src.services.text import TextService

text_service: TextService = TextService()
type_a_head_controller = TypeAHeadController(text_service=text_service)

# Create the FastAPI application
app = FastAPI()

#  Apply COR Configuration | https://fastapi.tiangolo.com/tutorial/cors/
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/v1/search/typeahead", status_code=status.HTTP_200_OK)
def type_a_head_handler(request: TypeAHeadRequest) -> TypeAHeadResponse:
    try:
        return type_a_head_controller.execute(request=request)
    except HTTPException as error:
        logging.error(str(error))
        raise error from error
    except Exception as error:
        # Caught all other uncaught errors.
        logging.error(str(error))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error"
        ) from error
