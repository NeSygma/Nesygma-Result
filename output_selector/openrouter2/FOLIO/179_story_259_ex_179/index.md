# Benchmark Report (SELECTOR): FOLIO - story_259_ex_179

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 3.78s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
All horses have hooves.
No humans have hooves.

Conclusion:
Some humans are horses.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to analyze the problem type and structure. The problem: Premises: All horses have hooves. No humans have hooves. Conclusion: Some humans are horses. We need to determine if conclusion is true, false, or uncertain. This is a typical categorical syllogism. We need to check entailment: Are the premises logically consistent with conclusion? The conclusion "Some humans are horses" is a categorical statement: ∃x (Human(x) ∧ Horse(x)). Premises: All horses have hooves: ∀x (Horse(x) → Hooves(x)). No humans have hooves: ∀x (Human(x) → ¬Hooves(x)). From these, we can deduce that no horse is human, because if a human had hooves, they'd be a horse? Wait, we have: All horses have hooves. No humans have hooves. That doesn't directly say that no horse is human. But we can deduce that if something is a horse, it has hooves. If something is a human, it does not have hooves. So a horse cannot be a human because a horse has hooves, a human does not. So the conclusion "Some humans are horses" is false. So answer: False. This is a typical entailment check. The solver that best fits: VAMPIRE, because it's about first-order logic entailment. CLINGO is for combinatorial search, not needed. Z3 is for constraint satisfaction with numeric constraints, not needed. So ranking: VAMPIRE > CLINGO > Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,272
  Output tokens: 359
  Total tokens:  1,631

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
