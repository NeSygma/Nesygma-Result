# Benchmark Report (SELECTOR): FOLIO - story_120_ex_70

**Provider:** openrouter3
**Model:** xiaomi/mimo-v2-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 2.82s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Badults is a British Sitcom series starring members of Pappy's.
Badults was piloted in July 2013 on BBC Three.
The Working title "The Secret Dude Society" was used for Badults.
Andrew Collins was the script editor for Badults.

Conclusion:
No members of Pappy's have starred in a show piloting on BBC Two or BBC Three.

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,280
  Output tokens: 24
  Total tokens:  1,304

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
