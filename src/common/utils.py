import tensorflow as tf


def custom_standardization(input_string):
    """Remove html line-break tags and handle punctuation"""

    lowercased = tf.strings.lower(input_string)
    # normalized_input = tf.strings.regex_replace(lowercased, "<br />", " ")
    # normalized_input = tf.strings.regex_replace(lowercased, "(')*('|\")", "")
    # return tf.strings.regex_replace(lowercased, f"([{string.punctuation}])", r" \1")
    return lowercased
