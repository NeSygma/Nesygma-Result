# Benchmark Report (SELECTOR): FOLIO - story_256_ex_46

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 3.94s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
All cats are mammals.
Some pets are not mammals.

Conclusion:
No pets are cats.

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,216
  Output tokens: 24
  Total tokens:  1,240

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
