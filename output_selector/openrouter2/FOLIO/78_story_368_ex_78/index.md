# Benchmark Report (SELECTOR): FOLIO - story_368_ex_78

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 3.55s


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

- We need to rank solvers. Problem: entailment checking from premises to conclusion. It's a natural-language logical entailment with quantifiers? Premises are universal statements about "people at Mary's school". They involve conditional statements. We need to determine if conclusion follows. This is a typical entailment problem. VAMPIRE is best for entailment. Clingo is for combinatorial search, not needed. Z3 is for constraints with numeric bounds, not needed. So ranking: VAMPIRE > CLINGO > Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}


### TOKEN USAGE

  Input tokens:  1,463
  Output tokens: 142
  Total tokens:  1,605

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

```
