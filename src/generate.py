from pydantic import BaseModel
from transformers import Pipeline, pipeline, set_seed


class Prediction(BaseModel):
    generated_text: str


class Predictions(BaseModel):
    results: list[Prediction]


if __name__ == "__main__":
    generator: Pipeline = pipeline("text-generation", model="gpt2")
    set_seed(42)

    results: Predictions = Predictions.parse_obj(
        {"results": generator("Hello, I'm a language model,", max_length=30, num_return_sequences=5)}
    )
    print(results.dict())
