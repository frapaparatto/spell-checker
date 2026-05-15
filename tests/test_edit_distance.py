import unittest
from algorithms.damerau_levenshtein import damerau_levenshtein_distance


class TestDamerauLevDistance(unittest.TestCase):
    def test_identical_strings(self):
        result = damerau_levenshtein_distance("hello", "hello", best_distance_found=3)
        self.assertEqual(result, 0)

    def test_empty_strings(self):
        result = damerau_levenshtein_distance("", "", best_distance_found=3)
        self.assertEqual(result, 0)

    def test_one_empty_string(self):
        result = damerau_levenshtein_distance("hello", "", best_distance_found=6)
        self.assertEqual(result, 5)

        result = damerau_levenshtein_distance("", "world", best_distance_found=6)
        self.assertEqual(result, 5)

    def test_single_insertion(self):
        result = damerau_levenshtein_distance("cat", "cats", best_distance_found=3)
        self.assertEqual(result, 1)

    def test_single_deletion(self):
        result = damerau_levenshtein_distance("cats", "cat", best_distance_found=3)
        self.assertEqual(result, 1)

    def test_single_substitution(self):
        result = damerau_levenshtein_distance("cat", "bat", best_distance_found=3)
        self.assertEqual(result, 1)

    def test_single_transposition(self):
        result = damerau_levenshtein_distance("hte", "the", best_distance_found=3)
        self.assertEqual(result, 1)

        result = damerau_levenshtein_distance("house", "hosue", best_distance_found=2)
        self.assertEqual(result, 1)

    def test_transposition_mid_word(self):
        # Transposition of 'l' and 'e' at positions 3-4 in a 5-letter word
        # "saels" = s-a-e-l-s, "sales" = s-a-l-e-s
        result = damerau_levenshtein_distance("saels", "sales", best_distance_found=3)
        self.assertEqual(result, 1)

    def test_transposition_counts_as_one_not_two(self):
        # Standard Levenshtein gives distance 2 for a transposition (delete + insert).
        # DL must give 1. If this returns 2, the algorithm is standard Levenshtein.
        result = damerau_levenshtein_distance("ab", "ba", best_distance_found=3)
        self.assertEqual(result, 1)

    def test_multiple_transpositions(self):
        result = damerau_levenshtein_distance("abcd", "badc", best_distance_found=3)
        self.assertEqual(result, 2)

    def test_complex_mixed_operations(self):
        result = damerau_levenshtein_distance(
            "kitten", "sitting", best_distance_found=4
        )
        self.assertEqual(result, 3)

    def test_symmetry(self):
        pairs = [
            ("hello", "helo"),
            ("cat", "bat"),
            ("hte", "the"),
            ("kitten", "sitting"),
            ("ab", "ba"),
        ]
        for a, b in pairs:
            with self.subTest(a=a, b=b):
                self.assertEqual(
                    damerau_levenshtein_distance(a, b, best_distance_found=10),
                    damerau_levenshtein_distance(b, a, best_distance_found=10),
                )

    def test_early_stop(self):
        result = damerau_levenshtein_distance("hello", "world", best_distance_found=2)
        self.assertIsNone(result)

        result = damerau_levenshtein_distance("cat", "bat", best_distance_found=1)
        self.assertEqual(result, 1)

        result = damerau_levenshtein_distance("cat", "bat", best_distance_found=0)
        self.assertIsNone(result)

        result = damerau_levenshtein_distance(
            "completely", "different", best_distance_found=3
        )
        self.assertIsNone(result)

    def test_early_stop_exact_threshold(self):
        # A word exactly at the threshold must be returned, not pruned.
        # "cat" vs "bat" is distance 1; best_distance_found=1 must return 1, not None.
        result = damerau_levenshtein_distance("cat", "bat", best_distance_found=1)
        self.assertEqual(result, 1)


if __name__ == "__main__":
    unittest.main()
