# Benchmark Report (SELECTOR): FOLIO - story_452_ex_29

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 3.36s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
All aliens are extraterrestrials.
If someone is from Mars, then they are an alien.
No extraterrestrials are human.
All highly intelligent beings from Earth are humans.
Marvin is a highly intelligent being.
Marvin is either from Earth and from Mars, or he is from neither.
If Marvin is not from Earth, then Marvin is an extraterrestrial.

Conclusion:
Marvin is neither a human nor from Mars.

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,288
  Output tokens: 24
  Total tokens:  1,312

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
