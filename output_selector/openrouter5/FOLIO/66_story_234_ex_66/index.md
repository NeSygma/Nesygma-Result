# Benchmark Report (SELECTOR): FOLIO - story_234_ex_66

**Provider:** openrouter5
**Model:** deepseek/deepseek-v4-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 3.07s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Yale University is a private Ivy League research university.
Yale University moved to New Haven in 1716.
Yale university's endowment was valued at $42.3 billion.
A list of residential colleges at Yale: Benjamin Franklin College, Berkeley College, Branford College, Davenport College, Ezra Stiles College, Grace Hopper College, Jonathan Edwards College, Morse College, Pauli Murray College, Pierson College, Saybrook College, Silliman College, Timothy Dwight College, and Trumbull College.

Conclusion:
A private Ivy League research university moved to New Haven.

Is the conclusion True, False, or Uncertain?

Based on the analysis of the problem structure, here is the ranking of the solvers:

The problem is a straightforward entailment check in first-order logic. It asks whether a specific conclusion ("A private Ivy League research university moved to New Haven") logically follows from a set of premises. The premises provide a specific instance (Yale University) that matches the description in the conclusion. This is a classic categorical syllogism with existential quantification, best handled by an automated theorem prover that operates under an open-world assumption and can handle universal and existential quantifiers.

```json
{
    "solver_ranking": ["VAMPIRE", "Z3", "CLINGO"]
}
```

### TOKEN USAGE

  Input tokens:  1,304
  Output tokens: 140
  Total tokens:  1,444

COMPLETE

## Selector Final Answer

```json
Based on the analysis of the problem structure, here is the ranking of the solvers:

The problem is a straightforward entailment check in first-order logic. It asks whether a specific conclusion ("A private Ivy League research university moved to New Haven") logically follows from a set of premises. The premises provide a specific instance (Yale University) that matches the description in the conclusion. This is a classic categorical syllogism with existential quantification, best handled by an automated theorem prover that operates under an open-world assumption and can handle universal and existential quantifiers.

```json
{
    "solver_ranking": ["VAMPIRE", "Z3", "CLINGO"]
}
```
```
