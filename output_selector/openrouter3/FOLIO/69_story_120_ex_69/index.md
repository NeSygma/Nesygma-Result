# Benchmark Report (SELECTOR): FOLIO - story_120_ex_69

**Provider:** openrouter3
**Model:** xiaomi/mimo-v2-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 1.71s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Badults is a British Sitcom series starring members of Pappy's.
Badults was piloted in July 2013 on BBC Three.
The Working title "The Secret Dude Society" was used for Badults.
Andrew Collins was the script editor for Badults.

Conclusion:
Andrew Collins was the script editor for a series with the working title "The Secret Dude Society".

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,279
  Output tokens: 24
  Total tokens:  1,303

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
