# Benchmark Report (SELECTOR): FOLIO - story_368_ex_78

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 8.51s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
If people at Mary's school work in student jobs on campus, then they need to earn money to help pay for their college tuition.
If people at Mary's school order takeout frequently in college, then they work in student jobs on campus.
People at Mary's school order takeout frequently in college or enjoy the dining hall meals and recipes.
If people at Mary's school enjoy the dining hall meals and recipes, then they are not picky eaters.
If people at Mary's school enjoy the dining hall meals and recipes, then they spend a lot of their time eating and catching up with friends in the campus dining halls.
Hannah is at Mary's school.
Hannah works in student jobs on campus and if she needs to earn money to help pay for her college tuition, then she is neither picky nor needs to earn money to help pay for her college tuition.

Conclusion:
Hannah is at Mary's school and she either is not a picky eater or, if she is, then she spends a lot of her time eating and catching up with friends in the campus dining halls.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to decide which solver is most suitable. The problem: natural language premises with conditionals, disjunctions, etc. Need to determine entailment (True/False/Uncertain) under open-world? The premises involve universal statements? They are generic statements about "people at Mary's school". It's like first-order logic with quantifiers (implicitly universal). The conclusion is about Hannah. This is typical entailment checking. No numeric counting, no combinatorial search. So VAMPIRE (FOL theorem prover) is best. CLINGO is for combinatorial search, not needed. Z3 could encode but not ideal. So ranking: VAMPIRE most suitable, then Z3 maybe, then CLINGO least. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "Z3", "CLINGO"]
}

### TOKEN USAGE

  Input tokens:  1,455
  Output tokens: 182
  Total tokens:  1,637

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "Z3", "CLINGO"]
}
```
