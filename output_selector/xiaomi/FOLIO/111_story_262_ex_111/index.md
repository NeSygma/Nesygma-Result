# Benchmark Report (SELECTOR): FOLIO - story_262_ex_111

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 3.10s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
All fir trees are evergreens.
Some objects of worship are fir trees.

Conclusion:
Some evergreens are not objects of worship.

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,224
  Output tokens: 24
  Total tokens:  1,248

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
