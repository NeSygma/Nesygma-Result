# Benchmark Report (SELECTOR): FOLIO - story_330_ex_130

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 3.35s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
All people who make wedding plans are people who are engaged.
All people who invite others to come to their ceremony make wedding plans.
Anyone who has a well-attended wedding invites others to come to their ceremony.
Some people that have well-attended weddings have larger families.
If John is engaged, then John does not invite friends to their ceremony and make wedding plans.
If John has a larger family, then either John has a well-attended wedding or invites friends to their ceremony. 

Conclusion:
John is engaged.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to rank solvers. Problem: It's a logical entailment problem with universal and existential quantifiers, categorical statements, and a conclusion about a specific individual John. We need to determine if conclusion is true, false, or uncertain. This is a typical entailment checking problem. VAMPIRE is best for entailment checking. CLINGO could also handle but it's more for combinatorial search. Z3 is for constraint satisfaction with numeric bounds. This problem is purely categorical logic, no numeric constraints. So ranking: VAMPIRE first, CLINGO second, Z3 third.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,356
  Output tokens: 151
  Total tokens:  1,507

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
