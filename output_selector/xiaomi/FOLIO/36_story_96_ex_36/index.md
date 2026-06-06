# Benchmark Report (SELECTOR): FOLIO - story_96_ex_36

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 4.92s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Diamond Mine is a professional wrestling stable formed in WWE.
Roderick Strong leads Diamond Mine.
Diamond Mine includes the Creed Brothers and Ivy Nile.
Imperium has a feud with Diamond Mine.

Conclusion:
Imperium doesn't have a feud with a professional wrestling stable that includes Ivy Nile.

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,257
  Output tokens: 24
  Total tokens:  1,281

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
