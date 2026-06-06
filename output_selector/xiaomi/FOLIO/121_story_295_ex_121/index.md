# Benchmark Report (SELECTOR): FOLIO - story_295_ex_121

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 5.38s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Some affection is love.
Some love is positive.

Conclusion:
Some affection is positive.

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
