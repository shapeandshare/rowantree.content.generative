import json
import string
from pathlib import Path

# Used to preprocess event.json files from The Rowan Tree into trainable entries


# # Leaves structure intact
# def process(file_in: str, file_out: str) -> None:
#     infile = Path(file_in)
#     outfile = Path(file_out)
#
#     with open(file=infile.resolve().as_posix(), mode="r", encoding="utf-8") as file:
#         in_data: dict = json.load(file)
#         out_data: str = ""
#         for event in in_data["events"]:
#             line_based_dict: dict = {"event": event}
#             newline_str = json.dumps(line_based_dict, sort_keys=True, indent=None)
#
#             newline_str = newline_str.replace("}", " }")
#             newline_str = newline_str.replace("{", "{ ")
#
#             out_data += newline_str + "\n"
#
#     with open(file=outfile.resolve().as_posix(), mode="w", encoding="utf-8") as file:
#         file.write(out_data)


# textual
def process(file_in: str, file_out: str) -> None:
    infile = Path(file_in)
    outfile = Path(file_out)

    with open(file=infile.resolve().as_posix(), mode="r", encoding="utf-8") as file:
        in_data: dict = json.load(file)
        out_data: str = ""
        for event in in_data["events"]:
            line_based_dict: dict = {"event": event}
            newline_str = json.dumps(line_based_dict, sort_keys=True, indent=None)

            # special cases, e.g. `-` --> ` `
            newline_str = newline_str.translate(str.maketrans("-", " "))

            # Remove punctuation
            newline_str = newline_str.translate(str.maketrans("", "", string.punctuation))

            # Remove extra white space
            newline_str = " ".join(newline_str.split())

            # Add line delimiter
            out_data += newline_str + "\n"

    with open(file=outfile.resolve().as_posix(), mode="w", encoding="utf-8") as file:
        file.write(out_data)


if __name__ == "__main__":
    process(file_in="assets/train/trt/events.json", file_out="train/trt/events_vocabulary.txt")
