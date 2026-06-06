# Benchmark Report (SELECTOR): FOLIO - story_361_ex_108

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 3.55s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
If people spill a lot of food on their clothing, then they are not notably tidy.
All clumsy foodies who go out frequently to find new food restaurants to try are people who spill a lot of food on their clothing.
If people are cleanly, then they are notably tidy.
If people value order and spotlessness, then they are cleanly.
All people whose families prioritize order and spotlessness themselves value order and spotlessness.
Peter is either a person who spills a lot of food on his clothing and is cleanly, or a person who does not spill a lot of food on his clothing and is not cleanly

Conclusion:
Peter is notably tidy.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to rank solvers. Problem: It's a logical entailment problem with categorical statements, universal quantifiers, and a conclusion about a specific individual. The premises involve "If people spill a lot of food on their clothing, then they are not notably tidy." etc. It's a typical first-order logic entailment. We need to determine if conclusion is true, false, or uncertain. This is a typical entailment checking problem. VAMPIRE is best for entailment checking. CLINGO is for combinatorial search, not needed. Z3 is for constraint satisfaction with numeric bounds, not needed. So ranking: VAMPIRE > CLINGO > Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,387
  Output tokens: 171
  Total tokens:  1,558

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
