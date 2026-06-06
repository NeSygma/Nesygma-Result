# Benchmark Report (SELECTOR): FOLIO - story_234_ex_67

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 3.95s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Yale University is a private Ivy League research university.
Yale University moved to New Haven in 1716.
Yale university's endowment was valued at $42.3 billion.
A list of residential colleges at Yale: Benjamin Franklin College, Berkeley College, Branford College, Davenport College, Ezra Stiles College, Grace Hopper College, Jonathan Edwards College, Morse College, Pauli Murray College, Pierson College, Saybrook College, Silliman College, Timothy Dwight College, and Trumbull College.

Conclusion:
Yale University has the largest university endowment of any educational institution.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to rank solvers. The problem: premises give facts about Yale University: private Ivy League, moved to New Haven, endowment $42.3B, list of residential colleges. Conclusion: "Yale University has the largest university endowment of any educational institution." We need to determine if conclusion is true, false, or uncertain. This is an entailment check: does the conclusion logically follow from premises? The premises do not provide any comparison to other institutions. So conclusion is uncertain. This is a typical entailment problem: we have a set of premises and a conclusion, we need to check entailment. This is exactly the domain of VAMPIRE: first-order logic entailment. The conclusion is a statement about a property of Yale relative to all institutions. The premises do not provide that. So it's uncertain. So the solver that best fits is VAMPIRE. CLINGO is for combinatorial search, not needed. Z3 is for constraint satisfaction with numeric bounds, not needed. So ranking: VAMPIRE > CLINGO > Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}


### TOKEN USAGE

  Input tokens:  1,373
  Output tokens: 253
  Total tokens:  1,626

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

```
