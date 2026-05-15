import cProfile
import json
import pstats
import sys

from corrector import query_tokenizer, suggest_correction
from utils import create_dictionary, get_max_distance, load_config, load_file


def main():
    try:
        config = load_config("./config.json")

    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(e)

        sys.exit()

    try:
        english_dictionary = create_dictionary(
            load_file(config["dictionary"]["english_path"])
        )
    except (ValueError, FileNotFoundError) as e:
        print(f"Error loading English dictionary: {e}")
        sys.exit()

    try:
        business_dictionary = create_dictionary(
            load_file(config["dictionary"]["business_path"])
        )
    except (ValueError, FileNotFoundError) as e:
        print(f"Error loading business dictionary: {e}")
        sys.exit()

    dictionary = english_dictionary | business_dictionary

    while True:
        research_query = input("Search (or 'quit' to exit): ").strip().lower()

        if research_query == "quit":
            print("Exiting")
            sys.exit()

        if not research_query:
            print("\nPlease, insert a search query.")
            continue

        with cProfile.Profile() as profile:
            suggestions = [
                suggest_correction(
                    query.strip(),
                    dictionary,
                    max_distance=get_max_distance(len(query), config),
                )
                for query in query_tokenizer(research_query)
                if query
            ]

            suggestion = " ".join(suggestions)
            print(f"Do you mean: {suggestion}")

        stats = pstats.Stats(profile).sort_stats(pstats.SortKey.TIME)
        stats.print_stats("corrector|utils|algorithms|main")


if __name__ == "__main__":
    main()
