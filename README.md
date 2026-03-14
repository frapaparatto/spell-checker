# Spell Checker Project

This project is a spell checker that suggests corrections for misspelled words. It uses the Damerau-Levenshtein distance algorithm to find the closest words in a dictionary.

## How it works

The spell checker takes a search query as input, tokenizes it into individual words, and then for each word, it searches for the closest match in a dictionary. The dictionary is a combination of a general English dictionary and a business-specific dictionary.

The suggestion logic is based on the Damerau-Levenshtein distance, which measures the similarity between two strings. The spell checker calculates the distance between the input word and each word in the dictionary. The word with the smallest distance is considered the best candidate for correction.

In cases where there are multiple words with the same minimum distance, the spell checker uses a probability-based approach to select the best correction. It calculates the probability of each candidate word based on its frequency in the dictionary and chooses the one with the highest probability.


## How to use

1. **Installation**: this project does not have any external dependencies. You only need Python 3 to run it.

2. **Running the spell checker**: to start the spell checker, run the `main.py` file:

   ```bash
   python main.py
   ```

   The program will prompt you to enter a search query. Type your query and press Enter. The spell checker will then provide suggestions for any misspelled words in the query.

   To exit the program, type `quit` and press Enter.
