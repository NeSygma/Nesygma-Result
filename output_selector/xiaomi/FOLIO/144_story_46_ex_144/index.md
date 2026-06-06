# Benchmark Report (SELECTOR): FOLIO - story_46_ex_144

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 3.99s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Breeding back is a form of artificial selection by the deliberate selective breeding of domestic animals.
Heck cattle were bred back in the 1920s to resemble the aurochs.
Heck cattle are animals.
Aurochs are animals.
Some animals to be bred back resemble extinct animals.

Conclusion:
Aurochs are extinct.

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,267
  Output tokens: 24
  Total tokens:  1,291

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
