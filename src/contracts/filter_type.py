from enum import Enum


class FilterType(str, Enum):
    UPPER = "upper"
    LOWER = "lower"
    NUMERIC = "numeric"
    PUNCTUATION = "punctuation"
    NEWLINE = "newline"
    LENGTH = "length"
    WHITESPACE = "whitespace"
