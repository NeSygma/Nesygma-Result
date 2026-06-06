# Benchmark Report (SELECTOR): FOLIO - story_234_ex_66

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 7.44s


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

- We need to rank solvers for this problem. The problem: given premises about Yale University being a private Ivy League research university, moved to New Haven in 1716, etc. Conclusion: "A private Ivy League research university moved to New Haven." This is a categorical entailment: from premises we have that Yale is a private Ivy League research university and moved to New Haven, so the conclusion is true (entailed). The problem is a simple entailment check with universal quantifiers? Actually it's about a specific individual: "Yale University is a private Ivy League research university" and "Yale University moved to New Haven". The conclusion is a generic statement: "A private Ivy League research university moved to New Haven." This is existential: there exists a private Ivy League research university that moved to New Haven. This is entailed by the premises. So it's a logical entailment problem, no numeric constraints, no combinatorial search. So VAMPIRE (first-order logic theorem prover) is best. CLINGO is for combinatorial search, not needed. Z3 is for numeric constraints, not needed. So ranking: VAMPIRE most suitable, then maybe CLINGO second (though could encode but not ideal), Z3 least.
- Thus output JSON with ranking: ["VAMPIRE","CLINGO","Z3"].


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,362
  Output tokens: 304
  Total tokens:  1,666

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
