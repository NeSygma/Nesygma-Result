# Benchmark Report (SELECTOR): FOLIO - story_51_ex_178

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 3.86s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
The summer Olympic games is a sporting event. 
The last summer Olympic games was in Tokyo.
The United States won the most medals in Tokyo. 

Conclusion:
The United States won the most medals in the last summer Olympic games.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to rank solvers based on problem type. The problem: natural language premises, conclusion, ask truth value (True/False/Uncertain). This is entailment checking with categorical reasoning, open-world assumption. That's exactly VAMPIRE's domain. No numeric counting or combinatorial search. So VAMPIRE most suitable. CLINGO is for combinatorial search, not needed. Z3 is for numeric constraints, not needed. So ranking: VAMPIRE, then maybe CLINGO, then Z3. Or CLINGO second, Z3 last. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,291
  Output tokens: 151
  Total tokens:  1,442

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
