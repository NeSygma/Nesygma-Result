# Benchmark Report (SELECTOR): FOLIO - story_51_ex_177

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 5.77s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
The summer Olympic games is a sporting event. 
The last summer Olympic games was in Tokyo.
The United States won the most medals in Tokyo. 

Conclusion:
The last summer Olympic games were not in Tokyo.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to rank solvers based on problem type. The problem: given premises, need to evaluate conclusion truth value (True/False/Uncertain). This is entailment checking. No numeric counting, no assignment. It's a simple natural language reasoning with categorical statements. This matches VAMPIRE best (first-order logic entailment). CLINGO is for combinatorial search, not needed. Z3 is for numeric constraints, not needed. So ranking: VAMPIRE most suitable, then maybe CLINGO second, Z3 least. Or CLINGO could also handle simple logical inference? But VAMPIRE is best. So ranking: ["VAMPIRE","CLINGO","Z3"].
- Return JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,287
  Output tokens: 178
  Total tokens:  1,465

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
