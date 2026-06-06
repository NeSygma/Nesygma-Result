# Benchmark Report (SELECTOR): FOLIO - story_340_ex_33

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 6.46s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Everyone at the mixer is a Grand Slam champion or an Oscar-nominated actor.
Every Grand Slam champion at the mixer is a professional tennis player.
All Oscar-nominated actors at the mixer are celebrities.
All professional tennis players at the mixer are athletes.
If a person at the mixer is a celebrity, then they are well paid.
If a person at the mixer is an athlete, then they are famous.
All well-paid people at the mixer live in tax havens.
Djokovic is at the mixer: if Djokovic is a famous athlete, then Djokovic is well-paid.

Conclusion:
Djokovic does not live in a tax haven.

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "Z3", "CLINGO"]
}

### TOKEN USAGE

  Input tokens:  1,332
  Output tokens: 24
  Total tokens:  1,356

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "Z3", "CLINGO"]
}
```
