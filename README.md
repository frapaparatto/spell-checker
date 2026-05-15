# Searchify

Searchify is a spelling correction engine for enterprise search: it detects and corrects user typing errors before a query reaches the search index.

## Design decisions

**Algorithm choice.** I chose Damerau-Levenshtein over standard Levenshtein because transpositions (e.g. "teh" → "the") are the most common real typing error, and Levenshtein counts them as two operations while Damerau-Levenshtein counts them as one, making the distance metric more accurate for this error distribution. Supported operations: insertion, deletion, substitution, transposition.

**Multi-word architecture.** I separated the engine into a single-word correction core and a query orchestrator because correcting one token at a time is not the real problem: users search with phrases like "raporto vendite 2023". The orchestrator tokenizes the full query, delegates each token to the core engine, and recombines the result. This allows independent testing of each layer.

**Correction vs suggestion.** Whether to present a correction as "Did you mean?" or silent auto-correction is a product decision, not an algorithm decision. The engine always returns the most probable correction; surfacing it is left to the caller.

**What this project does not do.** Search indexing, document ranking and retrieval, HTTP API, language detection: all explicitly out of scope.

## Configuration

Settings are loaded from `config.json` at startup.

| Parameter | Description |
|---|---|
| `max_distance_short` | Edit distance threshold for short words. Tighter bound prevents false positives. |
| `max_distance_long` | Edit distance threshold for long words. |

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

The dominant cost is `damerau_levenshtein_distance` (0.244 s of 0.405 s). The LRU cache on `_suggest_correction_cached` ensures each unique misspelling is corrected only once; `sum` is called twice (once per word), not inside any loop. Length pre-filtering via `abs` eliminates candidates before the expensive distance computation.

## License

MIT
