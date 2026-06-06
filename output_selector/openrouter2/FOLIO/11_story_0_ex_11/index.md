# Benchmark Report (SELECTOR): FOLIO - story_0_ex_11

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 1.75s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
There are six types of wild turkeys: Eastern wild turkey, Osceola wild turkey, Gould’s wild turkey, Merriam’s wild turkey, Rio Grande wild turkey, and Ocellated wild turkey.
Tom is not an Eastern wild turkey.
Tom is not an Osceola wild turkey.
Tom is not a Gould's wild turkey.
Tom is neither a Merriam's wild turkey nor a Rio Grande wild turkey.
Tom is a wild turkey.

Conclusion:
Tom is an Eastern wild turkey.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to rank solvers. Problem: Premises about categories, with negations. Conclusion: Tom is an Eastern wild turkey. We have premises: Tom is not Eastern, not Osceola, not Gould's, not Merriam's, not Rio Grande. Tom is a wild turkey. Conclusion: Tom is Eastern. This is a contradiction: premises say Tom is not Eastern, conclusion says Tom is Eastern. So conclusion is False. This is a simple categorical reasoning with universal negations. It's a first-order logic with unary predicates. We need to determine entailment: does conclusion follow? It's false. So we need a solver that can handle categorical reasoning with negations. VAMPIRE is best for entailment checking. CLINGO could also handle but it's more for combinatorial search. Z3 could encode but not necessary. So ranking: VAMPIRE > CLINGO > Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}


### TOKEN USAGE

  Input tokens:  1,353
  Output tokens: 218
  Total tokens:  1,571

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

```
