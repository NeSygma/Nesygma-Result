# Benchmark Report (SELECTOR): agieval_lsat - lsat_176

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 5.23s


 SELECTOR META EVALUATOR AGENT

 Query: Exactly five students—Grecia, Hakeem, Joe, Katya, and Louise—are to work at a campus art gallery during a special exhibit that runs for exactly five days, Monday through Friday. Each day is divided into two nonoverlapping shifts—first and second—with each student working exactly two shifts. Each shift is worked by exactly one of the students according to the following scheduling restrictions: No student works both shifts of any day. On two consecutive days, Louise works the second shift. On two nonconsecutive days, Grecia works the first shift. Katya works on Tuesday and Friday. Hakeem and Joe work on the same day as each other at least once. Grecia and Louise never work on the same day as each other.Q: Which one of the following must be true? Answer Choices: (A)Grecia does not work at the gallery on Tuesday. (B)Hakeem does not work at the gallery on Wednesday. (C)Joe does not work at the gallery on Tuesday. (D)Joe does not work at the gallery on Thursday. (E)Louise does not work at the gallery on Tuesday.
A: Among A through E, the answer is

{
    "solver_ranking": ["Z3", "CLINGO", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  1,434
  Output tokens: 24
  Total tokens:  1,458

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["Z3", "CLINGO", "VAMPIRE"]
}
```
