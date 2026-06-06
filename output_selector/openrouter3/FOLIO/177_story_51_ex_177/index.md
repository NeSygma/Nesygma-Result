# Benchmark Report (SELECTOR): FOLIO - story_51_ex_177

**Provider:** openrouter3
**Model:** xiaomi/mimo-v2-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 2.85s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
The summer Olympic games is a sporting event. 
The last summer Olympic games was in Tokyo.
The United States won the most medals in Tokyo. 

Conclusion:
The last summer Olympic games were not in Tokyo.

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,240
  Output tokens: 24
  Total tokens:  1,264

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
