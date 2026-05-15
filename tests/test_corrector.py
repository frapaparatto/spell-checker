import unittest
from typing import List

from corrector import _suggest_correction_cached, query_tokenizer, suggest_correction


class TestCorrector(unittest.TestCase):
    def setUp(self) -> None:
        self.dictionary = {
            "hello": 100,
            "world": 80,
            "hallo": 10,
            "help": 60,
            "held": 40,
            "sales": 150,
            "report": 200,
        }

    def tearDown(self) -> None:
        _suggest_correction_cached.cache_clear()

    # --- tokenizer ---

    def test_tokenize_single_word_query(self):
        result = query_tokenizer("suggestion")

        self.assertIsInstance(result, List)
        self.assertEqual(result, ["suggestion"])

    def test_tokenize_multi_words_query(self):
        result = query_tokenizer("sales report")

        self.assertIsInstance(result, List)
        self.assertListEqual(result, ["sales", "report"])

    def test_tokenize_empty_query(self):
        self.assertEqual(query_tokenizer(""), [])

    def test_tokenize_strips_extra_spaces(self):
        self.assertEqual(query_tokenizer("sales  report"), ["sales", "report"])

    # --- suggest_correction: exact match ---

    def test_correct_query_returns_same_word(self):
        result = suggest_correction("hello", self.dictionary, max_distance=2)

        self.assertEqual(result, "hello")

    # --- suggest_correction: probability tiebreak ---

    def test_same_distance_chooses_higher_probability(self):
        # "helo" is distance 1 from "hello" (100), "help" (60), "held" (40)
        result = suggest_correction("helo", self.dictionary, max_distance=2)

        self.assertEqual(result, "hello")

    # --- suggest_correction: transposition ---

    def test_transposition_is_corrected(self):
        # "saels" is one transposition away from "sales" (s-a-e-l-s vs s-a-l-e-s)
        # Standard Levenshtein would count this as distance 2; DL counts it as 1
        result = suggest_correction("saels", self.dictionary, max_distance=1)

        self.assertEqual(result, "sales")

    def test_transposition_distance_is_one_not_two(self):
        # Verify that a transposition candidate is preferred over a substitution
        # candidate when both exist and the transposition one has higher frequency.
        # "reprot" is one transposition from "report" (distance 1).
        result = suggest_correction("reprot", self.dictionary, max_distance=1)

        self.assertEqual(result, "report")

    # --- suggest_correction: no candidate ---

    def test_no_candidate_returns_original_query(self):
        # "zzz" has no dictionary word within any reasonable distance
        result = suggest_correction("zzz", self.dictionary, max_distance=2)

        self.assertEqual(result, "zzz")

    def test_zero_max_distance_never_corrects(self):
        # With max_distance=0 only exact matches are accepted
        result = suggest_correction("helo", self.dictionary, max_distance=0)

        self.assertEqual(result, "helo")


if __name__ == "__main__":
    unittest.main()
