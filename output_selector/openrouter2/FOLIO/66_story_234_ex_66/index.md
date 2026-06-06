# Benchmark Report (SELECTOR): FOLIO - story_234_ex_66

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 4.65s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Yale University is a private Ivy League research university.
Yale University moved to New Haven in 1716.
Yale university's endowment was valued at $42.3 billion.
A list of residential colleges at Yale: Benjamin Franklin College, Berkeley College, Branford College, Davenport College, Ezra Stiles College, Grace Hopper College, Jonathan Edwards College, Morse College, Pauli Murray College, Pierson College, Saybrook College, Silliman College, Timothy Dwight College, and Trumbull College.

Conclusion:
A private Ivy League research university moved to New Haven.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to rank solvers. The problem: premises list facts about Yale University. Conclusion: "A private Ivy League research university moved to New Haven." This is a general statement: "A private Ivy League research university moved to New Haven." We have premises: Yale University is a private Ivy League research university. Yale University moved to New Haven in 1716. So the conclusion is a generalization: "A private Ivy League research university moved to New Haven." This is a universal statement: For all X, if X is a private Ivy League research university, then X moved to New Haven. But we only have evidence for Yale. We cannot conclude that all such universities moved. So the conclusion is uncertain. This is a typical entailment checking problem: we need to determine if the conclusion logically follows from premises. This is a first-order logic entailment problem. So VAMPIRE is best. CLINGO is for combinatorial search, not needed. Z3 is for constraint satisfaction, not needed. So ranking: VAMPIRE > CLINGO > Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}


### TOKEN USAGE

  Input tokens:  1,370
  Output tokens: 253
  Total tokens:  1,623

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

```
