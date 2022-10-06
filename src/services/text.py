from math import floor
from typing import Optional

import pandas as pd
from transformers import Pipeline, pipeline, set_seed

from src.contracts.dtos.generation_parameters import GenerationParameters
from src.contracts.dtos.line_score import LineScore
from src.contracts.filter_type import FilterType


class TextService:
    generator: Pipeline

    def __init__(self):
        self.generator = pipeline("text-generation", model="gpt2")
        # set_seed()

    def execute(self, prompt: str, params: Optional[GenerationParameters] = None) -> list[str]:
        print(prompt)
        if params is None:
            params = GenerationParameters()
        print(params.json(by_alias=True))

        results: list[str] = []

        for i in range(params.epochs):
            max_length: int = floor(((i + 1) / params.epochs) * params.max_length) + len(prompt)

            predictions: list[dict[str, str]] = self.generator(
                prompt, max_length=max_length, num_return_sequences=params.num_responses
            )
            print(predictions)
            new_results: list[str] = [prediction["generated_text"] for prediction in predictions]
            results += new_results

        return TextService.post_process(results=results, quantile=params.quantile, filters=params.filters)

    @staticmethod
    def post_process(results: list[str], quantile: float, filters: list[FilterType]):
        score_df: pd.DataFrame = TextService.build_report(results=results)
        mean_quantile = score_df.loc[:, ~score_df.columns.isin(["text"])].quantile(quantile)
        filtered_df: pd.DataFrame = TextService.filter(
            results_df=score_df, mean_quantile=mean_quantile, filters=filters
        )
        return filtered_df["text"].tolist()

    @staticmethod
    def build_report(results: list[str]) -> pd.DataFrame:
        columns = ["text", "length", "lower", "upper", "numeric", "white_space", "punc", "total", "newline"]

        data_dict = {}
        for result in results:
            score = LineScore(text=result)
            score_dict = score.dict()

            for column in columns:
                if column not in data_dict:
                    data_dict[column] = [score_dict[column]]
                else:
                    data_dict[column].append(score_dict[column])

        return pd.DataFrame.from_dict(data_dict)

    @staticmethod
    def filter(results_df: pd.DataFrame, mean_quantile, filters: list[FilterType]) -> pd.DataFrame:
        filtered_df = results_df.copy(deep=True)

        if FilterType.UPPER in filters:
            filtered_df = filtered_df[filtered_df.upper <= mean_quantile.upper]
        if FilterType.LOWER in filters:
            filtered_df = filtered_df[filtered_df.lower <= mean_quantile.lower]
        if FilterType.NUMERIC in filters:
            filtered_df = filtered_df[filtered_df.numeric <= mean_quantile.numeric]
        if FilterType.PUNCTUATION in filters:
            filtered_df = filtered_df[filtered_df.punc <= mean_quantile.punc]
        if FilterType.NEWLINE in filters:
            filtered_df = filtered_df[filtered_df.newline <= mean_quantile.newline]
        if FilterType.LENGTH in filters:
            filtered_df = filtered_df[filtered_df.length <= mean_quantile.length]
        if FilterType.WHITESPACE in filters:
            filtered_df = filtered_df[filtered_df.white_space <= mean_quantile.white_space]

        return filtered_df
