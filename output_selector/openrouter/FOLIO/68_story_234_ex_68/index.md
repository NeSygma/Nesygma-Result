# Benchmark Report (SELECTOR): FOLIO - story_234_ex_68

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 5.54s


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

- We need to rank solvers. The problem: given premises about Yale, list of residential colleges includes Pierson College. The conclusion: Pierson College is a residential college at Yale. This is a straightforward entailment from a premise that lists Pierson College among residential colleges. This is a simple categorical entailment, no numeric constraints, no combinatorial search, no arithmetic. So best solver is VAMPIRE (first-order logic entailment). CLINGO could also handle but it's overkill; it's a closed-world logic programming, but could encode facts and query. Z3 is not needed. So ranking: VAMPIRE most suitable, then CLINGO, then Z3 least. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,361
  Output tokens: 174
  Total tokens:  1,535

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
