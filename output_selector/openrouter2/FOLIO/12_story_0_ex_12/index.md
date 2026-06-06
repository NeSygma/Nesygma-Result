# Benchmark Report (SELECTOR): FOLIO - story_0_ex_12

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 3.18s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
There are six types of wild turkeys: Eastern wild turkey, Osceola wild turkey, Gould’s wild turkey, Merriam’s wild turkey, Rio Grande wild turkey, and Ocellated wild turkey.
Tom is not an Eastern wild turkey.
Tom is not an Osceola wild turkey.
Tom is not a Gould's wild turkey.
Tom is neither a Merriam's wild turkey nor a Rio Grande wild turkey.
Tom is a wild turkey.

Conclusion:
Joey is a wild turkey.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to analyze the problem type. Premises: list of types of wild turkeys. Tom is not each type except unspecified. Tom is a wild turkey. Conclusion: Joey is a wild turkey. We have no information about Joey. So conclusion is uncertain. This is a typical entailment checking problem: given premises, does conclusion follow? It's a first-order logic with quantifiers? Actually we have individuals Tom and Joey, and predicates like "is a wild turkey" and "is an Eastern wild turkey". The premises say Tom is not each type, but Tom is a wild turkey. Conclusion says Joey is a wild turkey. There's no relation between Tom and Joey. So cannot entail. So answer: Uncertain.
- We need to rank solvers: VAMPIRE is best for entailment checking. CLINGO is for combinatorial search, not needed. Z3 is for constraint satisfaction with numeric constraints. So ranking: VAMPIRE > CLINGO > Z3.
- Thus output JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,353
  Output tokens: 234
  Total tokens:  1,587

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
