import os
import random
from pathlib import Path
from typing import List

import tensorflow as tf
from tensorflow.keras.layers import TextVectorization

from .utils import custom_standardization


def prepare_data(batch_size, vocab_size, maxlen):
    filenames: List[str] = []
    directories: List[str] = [os.environ["SM_CHANNEL_TRAIN"]]
    for dir in directories:
        print(f"Searching {dir} to load corpus..")
        for f in Path(dir).rglob("*.txt"):
            if f.is_file():
                filenames.append(f.resolve().as_posix())
                print(f"Adding {f.as_posix()} to corpus.")

    print(f"{len(filenames)} files")

    # Create a dataset from text files
    random.shuffle(filenames)
    text_ds = tf.data.TextLineDataset(filenames)
    text_ds = text_ds.shuffle(buffer_size=256)
    text_ds = text_ds.batch(batch_size)

    print("Elements of text_ds:")
    for x in text_ds:
        print(x)

    # Create a vectorization layer and adapt it to the text
    vectorize_layer = TextVectorization(
        standardize=custom_standardization,
        max_tokens=vocab_size - 1,
        output_mode="int",
        output_sequence_length=maxlen + 1,
    )
    vectorize_layer.adapt(text_ds)
    vocab = vectorize_layer.get_vocabulary()  # To get words back from token indices

    def prepare_lm_inputs_labels(text):
        """
        Shift word sequences by 1 position so that the target for position (i) is
        word at position (i+1). The model will use all words up till position (i)
        to generate the next word.
        """
        text = tf.expand_dims(text, -1)
        tokenized_sentences = vectorize_layer(text)
        x = tokenized_sentences[:, :-1]
        y = tokenized_sentences[:, 1:]
        return x, y

    text_ds = text_ds.map(prepare_lm_inputs_labels, num_parallel_calls=tf.data.AUTOTUNE)
    text_ds = text_ds.prefetch(tf.data.AUTOTUNE)

    return text_ds, vocab
