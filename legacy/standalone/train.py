RUN_OFFLINE: bool = True

if RUN_OFFLINE:
    from dotenv import load_dotenv

    # os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # or any {'0', '1', '2'}
    load_dotenv("env/.env.local")

import os

import tensorflow as tf

from legacy.standalone.common import prepare_data
from legacy.standalone.training.model import create_model


def train():
    epochs = 5000
    vocab_size = 20000  # Only consider the top 20k words
    maxlen = 128  # Max sequence size
    embed_dim = 256  # Embedding size for each token
    num_heads = 2  # Number of attention heads
    feed_forward_dim = 256  # Hidden layer size in feed forward network inside transformer

    batch_size = 256

    text_ds, vocab = prepare_data(batch_size=batch_size, vocab_size=vocab_size, maxlen=maxlen)

    model = create_model(
        maxlen=maxlen,
        vocab_size=vocab_size,
        embed_dim=embed_dim,
        num_heads=num_heads,
        feed_forward_dim=feed_forward_dim,
    )

    early_stop = tf.keras.callbacks.EarlyStopping(monitor="loss", patience=10, verbose=1)
    model.fit(text_ds, verbose=2, epochs=epochs, callbacks=[early_stop])
    tf.keras.models.save_model(model=model, filepath=os.environ["SM_MODEL_DIR"])


if __name__ == "__main__":
    train()
