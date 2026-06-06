# Benchmark Report (SELECTOR): FOLIO - story_203_ex_137

**Provider:** openrouter5
**Model:** deepseek/deepseek-v4-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 1.77s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Plungers suck.
Vacuums suck.
Vampires suck.
Space is a vacuum.
A duster is a household appliance that doesn't suck.

Conclusion:
If something is a household appliance, it sucks.

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,232
  Output tokens: 24
  Total tokens:  1,256

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
