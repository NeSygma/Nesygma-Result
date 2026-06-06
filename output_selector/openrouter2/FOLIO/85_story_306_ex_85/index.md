# Benchmark Report (SELECTOR): FOLIO - story_306_ex_85

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 3.40s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
If a restaurant is listed in Yelp’s recommendations, then the restaurant has not received many negative reviews.
All restaurants with a rating greater than four are listed in Yelp’s recommendations.
Some restaurants that do not provide take-out service receive many negative reviews.
All restaurants that are popular among local residents have ratings greater than four.
The Hamden Plaza Subway store has a rating greater than four, or it is popular among local residents.

Conclusion:
The Hamden Plaza Subway store provides take-out service or does not receive many negative reviews.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to rank solvers. Problem: It's a logical entailment problem with categorical statements, universal and existential quantifiers, and a conclusion about a specific entity. We need to determine if conclusion is true, false, or uncertain. This is a typical entailment checking problem. VAMPIRE is best for entailment. Clingo is for combinatorial search, not needed. Z3 is for constraint satisfaction with numeric bounds, not needed. So ranking: VAMPIRE > CLINGO > Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,357
  Output tokens: 138
  Total tokens:  1,495

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
