import json
import os
import re
from collections import Counter
from typing import Dict


def load_file(filepath: str) -> str:
    if not filepath or not os.path.exists(filepath):
        raise FileNotFoundError(f"File '{filepath}' not found.")

    with open(filepath, "r") as file:
        text = file.read()

    return text


def create_dictionary(text: str) -> Dict[str, int]:
    """Create a dictionary of word with their frequencies from a text file."""
    if not text:
        raise ValueError("Text file is empty, can't create the dictionary.")

    words = re.findall(r"\w+", text.lower())  # list of words
    # return a dictionary with the count of all occurrences of each word
    return Counter(words)


def get_max_distance(len_query: int, config: Dict) -> int:
    """Use different values for the max edit distance based on the length of the word"""

    return (
        config["algorithm"]["max_distance_long"]
        if len_query >= 4
        else config["algorithm"]["max_distance_short"]
    )


def load_config(filepath: str) -> Dict:
    if not filepath or not os.path.exists(filepath):
        raise FileNotFoundError(f"File '{filepath}' not found.")

    with open(filepath, "r") as file:
        return json.load(file)
