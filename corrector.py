import functools
from typing import Dict, List, Tuple
from algorithms.damerau_levenshtein import damerau_levenshtein_distance


def query_tokenizer(query: str) -> List[str]:
    """Split a multi-word query into individual tokens."""
    return query.split()


def calculate_probability(word: str, words: Dict[str, int], total_words: int) -> float:
    """Calculate the probability of each single word in the dictionary."""
    return words[word] / total_words


@functools.lru_cache(maxsize=128)
def _suggest_correction_cached(
    query: str, dictionary: Tuple[Tuple[str, int], ...], max_distance: int
) -> str:
    dict_lookup = dict(dictionary)

    if query in dict_lookup:
        return query

    total_words = sum(dict_lookup.values())
    candidates = []
    best_distance_found = max_distance

    for word in dict_lookup:
        if abs(len(word) - len(query)) > max_distance:
            continue

        distance = damerau_levenshtein_distance(query, word, best_distance_found)

        if distance is None:
            continue

        if distance <= best_distance_found:
            candidates.append((word, distance))

        if distance < best_distance_found:
            best_distance_found = distance

    if not candidates:
        return query

    best_candidates = [
        word for word, distance in candidates if distance == best_distance_found
    ]

    return max(best_candidates, key=lambda x: calculate_probability(x, dict_lookup, total_words))


def suggest_correction(
    query: str, dictionary: Dict[str, int], max_distance: int
) -> str:
    """Main correction function."""
    return _suggest_correction_cached(query, tuple(sorted(dictionary.items())), max_distance)
