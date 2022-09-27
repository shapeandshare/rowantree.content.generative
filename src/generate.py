RUN_OFFLINE: bool = True

if RUN_OFFLINE:
    from dotenv import load_dotenv

    # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
    load_dotenv("env/.env.local")

import tarfile
import tempfile
from pathlib import Path

import tensorflow as tf

from .common.data import prepare_data
from .predict.text_generator import TextGenerator


def generate():
    # maxlen = 128  # Max sequence size
    maxlen = 256  # Max sequence size
    vocab_size = 20000  # Only consider the top 20k words
    batch_size = 256

    text_ds, vocab = prepare_data(batch_size=batch_size, vocab_size=vocab_size, maxlen=maxlen)

    print("-- Vocab --")
    print(vocab)

    # Tokenize starting prompt
    word_to_index = {}
    for index, word in enumerate(vocab):
        word_to_index[word] = index

    model_filepath: str = (Path(".") / "models" / "trt" / "model.tar.gz").resolve().as_posix()
    with tarfile.open(name=model_filepath, mode="r:*") as model_tar:
        with tempfile.TemporaryDirectory() as tmpdirname:
            model_tar.extractall(path=tmpdirname)
            restored_model = tf.keras.models.load_model(filepath=tmpdirname)

    prompt_string = "{\n" '  "events": [\n'

    prompts: list[str] = [prompt_string]
    # prompts: list[str] = ["robot", "raccoon", "spider"]
    # prompts: list[str] = ["What are you?", "How do you feel?", "What do you want?"]
    # prompts: list[str] = ["S"]
    complete_text: str = ""
    GEN_CYCLES = 1
    for start_prompt in prompts:
        print(f"-- Prompt --")
        print(start_prompt)
        # complete_text += start_prompt + "\n"

        start_tokens = [word_to_index.get(_, 1) for _ in start_prompt.split()]
        print("-- Start Tokens --")
        print(start_tokens)

        NUM_TOKENS_GENERATED = 256

        restored_generator = TextGenerator(
            max_tokens=NUM_TOKENS_GENERATED,
            maxlen=maxlen,
            start_tokens=start_tokens,
            index_to_word=vocab,
            model=restored_model,
        )

        def generate():
            txt = restored_generator.generate()
            txt = txt.replace("[UNK]", "")
            txt = txt.strip()
            return txt

        for i in range(0, GEN_CYCLES):
            complete_text += generate() + "\n\n"

    print(complete_text)


if __name__ == "__main__":
    generate()
