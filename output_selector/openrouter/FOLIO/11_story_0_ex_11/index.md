# Benchmark Report (SELECTOR): FOLIO - story_0_ex_11

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 6.99s


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

- We need to rank solvers based on problem type. The problem: premises about categories (type of wild turkey) and a conclusion about membership. It's a categorical reasoning with universal/negation statements about a specific individual. No numeric constraints, no planning, no ordering. It's about entailment: given premises, does conclusion follow? This is classic first-order logic entailment with open-world assumption? The premises say Tom is not any of the six types, but also says Tom is a wild turkey. There are six types of wild turkeys, presumably exhaustive categories? The premises do not state that every wild turkey is one of those six types, but it's implied by "There are six types of wild turkeys". That is a universal statement: For any wild turkey, it belongs to one of those six types. Under open-world assumption, we need to see if that is encoded. VAMPIRE is best for entailment with quantifiers. CLINGO is for combinatorial search, not needed. Z3 could encode but not needed. So ranking: VAMPIRE most suitable, then maybe Z3 (could encode but less natural), then CLINGO least.
- Thus output JSON with ranking: ["VAMPIRE","Z3","CLINGO"]


{
    "solver_ranking": ["VAMPIRE", "Z3", "CLINGO"]
}

### TOKEN USAGE

  Input tokens:  1,345
  Output tokens: 285
  Total tokens:  1,630

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "Z3", "CLINGO"]
}
```
