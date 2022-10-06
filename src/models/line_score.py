import string
import traceback
from typing import Any, Optional

from src.models.base_model import BaseModel


class LineScore(BaseModel):
    text: str
    length: Optional[int]
    # float (0->1) percentage of the string
    lower: Optional[float]
    upper: Optional[float]
    numeric: Optional[float]
    white_space: Optional[float]
    punc: Optional[float]
    total: Optional[float]
    newline: Optional[float]

    def __init__(self, **data: Any):
        super().__init__(**data)

        self.length: int = len(self.text)
        white_space_count: int = len([i for i in self.text if i.isspace()])
        punc_count: int = len([i for i in self.text if i in string.punctuation])
        digits_count: int = len([i for i in self.text if i in string.digits])
        lower_count: int = len([i for i in self.text if i in string.ascii_lowercase])
        upper_count: int = len([i for i in self.text if i in string.ascii_uppercase])
        newline_count: int = len([i for i in self.text if i == "\n"])

        self.lower = lower_count / self.length
        self.upper = upper_count / self.length
        self.numeric = digits_count / self.length
        self.white_space = white_space_count / self.length
        self.punc = punc_count / self.length
        self.newline = newline_count / self.length

        try:
            self.total = self.lower + self.upper + self.numeric + self.white_space + self.punc + self.newline
        except Exception as error:
            traceback.print_exc()
            print(self.text)
            raise error
