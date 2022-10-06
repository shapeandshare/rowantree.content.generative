""" Abstract Controller Definition """
from abc import abstractmethod
from typing import Any, Optional

from src.contracts.dtos.base_model import BaseModel


class AbstractController(BaseModel):
    """
    Abstract Controller
    """

    @abstractmethod
    def execute(self, *args, **kwargs) -> Optional[Any]:
        """Should be implemented in the subclass"""
