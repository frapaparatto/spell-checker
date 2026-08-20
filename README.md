# Spellchecker

A spelling correction engine for search queries: it detects and corrects typing errors before a query reaches the search index.

## Design decisions

**Algorithm choice.** Damerau-Levenshtein distance, not standard Levenshtein, because transpositions ("teh" -> "the") are the most common typing error. Levenshtein counts a transposition as two operations; Damerau-Levenshtein counts it as one, which makes the distance metric a better fit for this error distribution. Supported operations: insertion, deletion, substitution, transposition.

**Multi-word architecture.** The engine is split into a single-word correction core and a query orchestrator, because correcting one token at a time isn't the real problem: users search with phrases like "raporto vendite 2023". The orchestrator tokenizes the full query, delegates each token to the core engine, and recombines the result. Splitting the layers keeps each one independently testable.

**Correction vs. suggestion.** Whether to present a correction as "Did you mean?" or apply it silently is a product decision, not an algorithm one. The engine always returns its most probable correction; how that's surfaced is left to the caller.

**Out of scope.** Search indexing, document ranking and retrieval, an HTTP API, and language detection.

## Configuration

Settings are loaded from `config.json` at startup.

| Parameter | Description |
|---|---|
| `dictionary.english_path` | Path to the general-purpose word list. |
| `dictionary.business_path` | Path to the domain-specific word list, merged with the English one. |
| `algorithm.max_distance_short` | Edit distance threshold for short words. A tighter bound prevents false positives on short strings. |
| `algorithm.max_distance_long` | Edit distance threshold for long words. |

## Usage

```
python main.py
```

Enter a search query at the prompt. Type `quit` to exit.

```
Search (or 'quit' to exit): sles reprt
Do you mean: sales report
```

No external dependencies. Requires Python 3.10+.

## Testing

```
python -m unittest discover tests/ -v
```

32 tests across three modules: the Damerau-Levenshtein algorithm, the correction engine, and the utility functions.

## Benchmark

cProfile output for the query `"sles reprt"`:

```
947540 function calls in 0.405 seconds

ncalls  tottime  percall  cumtime  percall  function
27601   0.244    0.000    0.319    0.000    damerau_levenshtein_distance
    2   0.044    0.022    0.375    0.188    _suggest_correction_cached
357733  0.043    0.000    0.043    0.000    min (builtin)
496603  0.040    0.000    0.040    0.000    len (builtin)
    2   0.024    0.012    0.024    0.012    sorted (builtin)
    2   0.005    0.002    0.405    0.202    suggest_correction
65482   0.005    0.000    0.005    0.000    abs (builtin)
    2   0.000    0.000    0.000    0.000    sum (builtin)
```

`damerau_levenshtein_distance` dominates the cost (0.244 s of 0.405 s). The LRU cache on `_suggest_correction_cached` means each unique misspelling is corrected only once; `sum` is called twice (once per word), not inside a loop. Length pre-filtering via `abs` eliminates candidates before the expensive distance computation.

## License

MIT
