# Searchify

Searchify is a spelling correction engine for enterprise search: it detects and corrects user typing errors before a query reaches the search index.

## Design decisions

**Algorithm choice.** I chose Damerau-Levenshtein over standard Levenshtein because transpositions (e.g. "teh" → "the") are the most common real typing error, and Levenshtein counts them as two operations while Damerau-Levenshtein counts them as one, making the distance metric more accurate for this error distribution. Supported operations: insertion, deletion, substitution, transposition.

**Multi-word architecture.** I separated the engine into a single-word correction core and a query orchestrator because correcting one token at a time is not the real problem — users search with phrases like "raporto vendite 2023". The orchestrator tokenizes the full query, delegates each token to the core engine, and recombines the result. This allows independent testing of each layer.

**Correction vs suggestion.** Whether to present a correction as "Did you mean?" or silent auto-correction is a product decision, not an algorithm decision. The engine always returns the most probable correction; surfacing it is left to the caller.

**What this project does not do.** Search indexing, document ranking and retrieval, HTTP API, language detection — all explicitly out of scope.

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

## Benchmark

cProfile output for the query `"sles reprt"`:

```
929966 function calls in 0.522 seconds

ncalls  tottime  percall  cumtime  percall  function
27601   0.303    0.000    0.440    0.000    damerau_levenshtein_distance
355608  0.098    0.000    0.098    0.000    min (builtin)
481145  0.056    0.000    0.056    0.000    len (builtin)
2       0.054    0.027    0.521    0.261    suggest_correction
65482   0.008    0.000    0.008    0.000    abs (builtin)
9       0.004    0.000    0.004    0.000    sum (builtin)
```

The dominant cost is `damerau_levenshtein_distance` (0.303 s of 0.522 s). `sum(words.values())` is called 9 times inside the suggestion loop — this is constant data and is the identified bottleneck (see Improvements).

## Improvements

Three targeted improvements identified from profiling, each self-contained:

**1. Pre-compute corpus size.** `sum(words.values())` runs inside the suggestion loop on every call. It is constant data. Moving it to load time eliminates 9 redundant sum calls per 2-word query and more for longer queries.

**2. LRU cache on `suggest_correction`.** `@functools.lru_cache` on the single-word correction function caches results for repeated misspellings (e.g. "raporto" computed once). Zero logic change, one decorator.

**3. BK-Tree for candidate lookup.** Current candidate search is O(n) over the full dictionary. A Burkhard-Keller Tree exploits the triangle inequality of the metric space to prune candidates, reducing lookup to O(log n). Trade-off: higher initialization cost, faster repeated queries. Worthwhile at 100k+ word dictionaries.

## License

MIT
