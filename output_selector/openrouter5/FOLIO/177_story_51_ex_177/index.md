# Benchmark Report (SELECTOR): FOLIO - story_51_ex_177

**Provider:** openrouter5
**Model:** deepseek/deepseek-v4-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 1.50s


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

  Input tokens:  1,230
  Output tokens: 24
  Total tokens:  1,254

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
