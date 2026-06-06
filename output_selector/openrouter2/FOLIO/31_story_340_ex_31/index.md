# Benchmark Report (SELECTOR): FOLIO - story_340_ex_31

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 1.79s


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
Djokovic is a Grand Slam champion.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to rank solvers: VAMPIRE, CLINGO, Z3. The problem is a logical entailment: premises about categories, universal quantifiers, and a specific individual Djokovic. We need to determine if conclusion is true, false, or uncertain. This is a typical entailment checking problem with universal quantifiers, predicates, and a conditional about Djokovic. The conclusion is a specific statement about Djokovic. This is a first-order logic entailment problem. VAMPIRE is best for this. CLINGO is for combinatorial search, not needed. Z3 is for constraint satisfaction with numeric bounds, not needed. So ranking: VAMPIRE > CLINGO > Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,377
  Output tokens: 176
  Total tokens:  1,553

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
