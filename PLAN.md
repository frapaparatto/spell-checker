# PLAN.md

## Section 1: README Instructions

### Project description
One sentence. State what the engine does and why it exists, naming the domain.
Exact phrasing: "Searchify is a spelling correction engine for enterprise search: it detects and corrects user typing errors before a query reaches the search index."
Avoid: "powerful", "robust", "easy-to-use", "feature-rich", any list of bullets describing what it does.

### Design decisions
Use "I chose X because Y" framing. Cover at minimum:

**Algorithm choice:**
Write: "I chose Damerau-Levenshtein over standard Levenshtein because transpositions (e.g. 'teh' → 'the') are the most common real typing error, and Levenshtein counts them as two operations while Damerau-Levenshtein counts them as one, making the distance metric more accurate for this error distribution."

**Multi-word architecture:**
Write: "I separated the engine into a single-word correction core and a query orchestrator because correcting one token at a time is not the real problem — users search with phrases like 'raporto vendite 2023'. The orchestrator tokenizes the full query, delegates each token to the core engine, and recombines the result. This allows independent testing of each layer."

**Correction vs suggestion:**
Write: "Whether to present a correction as 'Did you mean?' or silent auto-correction is a product decision, not an algorithm decision. The engine always returns the most probable correction; surfacing it is left to the caller."

Avoid: "clean architecture", "scalable", "extensible", "best practices".

### Configuration
List the two JSON parameters with a one-line description each:
- `max_distance_short`: edit distance threshold for short words (tighter, prevents false positives)
- `max_distance_long`: edit distance threshold for long words

State: "Settings are loaded from `config.json` at startup."

### Usage
Imperative CLI-style. Show the exact command to run the engine, not prose.
Example format:
```
python main.py
```
No sub-bullets. No explanatory prose beyond one sentence if truly needed.

### Benchmark
Instruct: paste the raw cProfile block verbatim from the context file. Add one sentence below it:
"The dominant cost is `damerau_levenshtein_distance` (0.303 s of 0.522 s). `sum(words.values())` is called 9 times inside the suggestion loop — this is constant data and is the identified bottleneck (see Improvements)."
Do not interpret further.

### AI usage
Reflect the rules from the context file accurately and completely. Do not soften or generalize. Use the same framing.
Cover: read docs and form hypothesis first; try two or three approaches before AI; 20-minute timer rule; Socratic use only; always have a position before asking; AI does not replace debugging or reading docs; for boilerplate: only when concept is mastered, one function at a time, comment-specs first, read and explain every line before committing.

### Contributing
One sentence: "Open an issue before submitting a pull request."

### License
One sentence stating the license type (MIT or as applicable). Do not add a block of license text.

---

## Section 2: Code Improvements

### Improvement 1 — Pre-compute corpus size
**What it does:** Moves `sum(words.values())` out of the per-query suggestion loop and computes it once at corpus load time, storing it as a module-level or instance variable.
**Where it plugs in:** `corrector.py`, wherever `suggest_correction` computes `count / total_words` — replace the inline `sum(words.values())` call with a pre-computed `total_words` variable initialized when the dictionary is loaded.
**Why it matters:** The profiler shows 9 `sum` calls for a 2-word query. This is constant data recomputed on every call. Eliminating it is the lowest-risk, highest-signal optimization: it demonstrates reading profiler output and acting on it rather than guessing.

### Improvement 2 — LRU cache on suggest_correction
**What it does:** Adds `@functools.lru_cache` to the single-word correction function so repeated lookups for the same misspelled token (e.g. "raporto") are served from cache.
**Where it plugs in:** One decorator line above `suggest_correction` in `corrector.py`. Requires the function signature to use only hashable arguments (string input, no mutable defaults).
**Why it matters:** Shows awareness of memoization as an O(1) amortized fix for repeated queries, and that the candidate knew when to reach for a stdlib tool rather than rolling a custom solution.

### Improvement 3 — Weighted substitution cost
**What it does:** Introduces a `get_weighted_cost(c1, c2)` function that returns 0.5 for QWERTY keyboard-adjacent character pairs and 1.0 otherwise, used in place of the fixed substitution cost of 1 inside the Damerau-Levenshtein matrix.
**Where it plugs in:** Inside `damerau_levenshtein_distance` in `algorithms/`, at the substitution cost assignment. Define the adjacency map as a module-level constant (dict of char → set of adjacent chars).
**Why it matters:** The algorithm accounts for the physical layout of input, not just abstract string distance — a concrete improvement to correction accuracy that demonstrates domain thinking, not just coding.
