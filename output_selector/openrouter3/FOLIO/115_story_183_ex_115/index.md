# Benchmark Report (SELECTOR): FOLIO - story_183_ex_115

**Provider:** openrouter3
**Model:** xiaomi/mimo-v2-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 1.57s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
If a man is taller than another man, the taller one can block the other's shooting.
Michael is a man who is taller than everyone else in his class.
If person x is taller than person y, and person y is taller than person z, then x is taller than z
Peter is a man who is taller than Michael.
Michael can block any shooting from a person as long as the person does not jump when shooting.
Michael cannot block Windy's shooting.
Every shooter who can jump when shooting is a great shooter.

Conclusion:
Peter is shorter than a man in Michael's class.

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,318
  Output tokens: 24
  Total tokens:  1,342

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
