import unittest

from utils import create_dictionary, get_max_distance


class TestCreateDictionary(unittest.TestCase):
    def test_word_frequencies(self):
        result = create_dictionary("the cat sat the cat")
        self.assertEqual(result["the"], 2)
        self.assertEqual(result["cat"], 2)
        self.assertEqual(result["sat"], 1)

    def test_lowercases_input(self):
        result = create_dictionary("Hello WORLD hello")
        self.assertEqual(result["hello"], 2)
        self.assertEqual(result["world"], 1)

    def test_strips_punctuation(self):
        result = create_dictionary("hello, world! hello.")
        self.assertIn("hello", result)
        self.assertNotIn("hello,", result)
        self.assertNotIn("world!", result)

    def test_empty_text_raises(self):
        with self.assertRaises(ValueError):
            create_dictionary("")

    def test_single_word(self):
        result = create_dictionary("hello")
        self.assertEqual(result["hello"], 1)
        self.assertEqual(len(result), 1)


class TestGetMaxDistance(unittest.TestCase):
    CONFIG = {
        "algorithm": {
            "max_distance_short": 1,
            "max_distance_long": 2,
        }
    }

    def test_short_word_uses_short_threshold(self):
        self.assertEqual(get_max_distance(3, self.CONFIG), 1)

    def test_long_word_uses_long_threshold(self):
        self.assertEqual(get_max_distance(4, self.CONFIG), 2)
        self.assertEqual(get_max_distance(10, self.CONFIG), 2)

    def test_boundary_at_four_characters(self):
        self.assertEqual(get_max_distance(3, self.CONFIG), 1)
        self.assertEqual(get_max_distance(4, self.CONFIG), 2)


if __name__ == "__main__":
    unittest.main()
