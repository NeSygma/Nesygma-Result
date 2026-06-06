# Benchmark Report (SELECTOR): FOLIO - story_258_ex_156

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 10.92s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
All humans are mortal.
All Greeks are humans.

Conclusion:
Some Greeks are mortal.

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,215
  Output tokens: 24
  Total tokens:  1,239

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
