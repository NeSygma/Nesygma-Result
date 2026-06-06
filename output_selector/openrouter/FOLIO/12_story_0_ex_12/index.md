# Benchmark Report (SELECTOR): FOLIO - story_0_ex_12

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 6.82s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
There are six types of wild turkeys: Eastern wild turkey, Osceola wild turkey, Gould’s wild turkey, Merriam’s wild turkey, Rio Grande wild turkey, and Ocellated wild turkey.
Tom is not an Eastern wild turkey.
Tom is not an Osceola wild turkey.
Tom is not a Gould's wild turkey.
Tom is neither a Merriam's wild turkey nor a Rio Grande wild turkey.
Tom is a wild turkey.

Conclusion:
Joey is a wild turkey.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to rank solvers. The problem: premises about types of wild turkeys, statements about Tom not being any of the six types, but Tom is a wild turkey. Conclusion: Joey is a wild turkey. This is a reasoning about categories and individuals. No numeric constraints. It's about entailment: does the conclusion follow from premises? Premises only talk about Tom, not Joey. So conclusion is uncertain (cannot be derived nor contradicted). This is a typical entailment checking with open-world assumption. VAMPIRE is best for such categorical reasoning. CLINGO is for combinatorial search, not needed. Z3 is for numeric constraints, not needed. So ranking: VAMPIRE most suitable, then CLINGO, then Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,345
  Output tokens: 188
  Total tokens:  1,533

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
