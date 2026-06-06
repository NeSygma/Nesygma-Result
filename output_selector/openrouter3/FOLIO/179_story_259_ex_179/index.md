# Benchmark Report (SELECTOR): FOLIO - story_259_ex_179

**Provider:** openrouter3
**Model:** xiaomi/mimo-v2-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 9.06s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
All horses have hooves.
No humans have hooves.

Conclusion:
Some humans are horses.

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,217
  Output tokens: 24
  Total tokens:  1,241

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
