# Benchmark Report (SELECTOR): FOLIO - story_20_ex_15

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 8.35s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
A Japanese game company created the game the Legend of Zelda.
All games on the Top 10 list are made by Japanese game companies.
If a game sells more than one million copies, then it will be included in the Top 10 list.
The Legend of Zelda sold more than one million copies.

Conclusion:
The Legend of Zelda is not on the Top 10 list.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to rank solvers. The problem: natural language premises with universal statements, conditional, and a conclusion. It's a logical entailment question: determine if conclusion follows, contradicts, or uncertain. This is typical for VAMPIRE (first-order logic entailment). Not about numeric counting or assignment, not combinatorial search. So VAMPIRE is most suitable. CLINGO could encode but it's not natural; but it's not about combinatorial search. Z3 also could but it's not numeric constraints, just logical entailment. So ranking: VAMPIRE > CLINGO > Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,320
  Output tokens: 157
  Total tokens:  1,477

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
