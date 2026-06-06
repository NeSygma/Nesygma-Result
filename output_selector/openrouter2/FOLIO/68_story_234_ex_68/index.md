# Benchmark Report (SELECTOR): FOLIO - story_234_ex_68

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 3.89s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Yale University is a private Ivy League research university.
Yale University moved to New Haven in 1716.
Yale university's endowment was valued at $42.3 billion.
A list of residential colleges at Yale: Benjamin Franklin College, Berkeley College, Branford College, Davenport College, Ezra Stiles College, Grace Hopper College, Jonathan Edwards College, Morse College, Pauli Murray College, Pierson College, Saybrook College, Silliman College, Timothy Dwight College, and Trumbull College.

Conclusion:
Pierson College is a residential college at Yale.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to rank solvers. The problem: premises list facts about Yale University, including a list of residential colleges. Conclusion: Pierson College is a residential college at Yale. This is a straightforward entailment check: given the list includes Pierson College, the conclusion is true. This is a simple categorical entailment. So VAMPIRE is best: first-order logic entailment. Clingo could also handle but it's more for combinatorial search. Z3 is for constraints, not needed. So ranking: VAMPIRE > CLINGO > Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,369
  Output tokens: 149
  Total tokens:  1,518

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
