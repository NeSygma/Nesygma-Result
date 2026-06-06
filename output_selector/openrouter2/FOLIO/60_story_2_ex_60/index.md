# Benchmark Report (SELECTOR): FOLIO - story_2_ex_60

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 3.33s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Billings is a city in the state of Montana in U.S.
The state of Montana includes the cities of Butte, Helena, and Missoula.
White Sulphur Springs and Butte are cities in the same state in U.S.
The city of St Pierre is not in the state of Montana.
Any city in Butte is not in St Pierre.
A city can only be in one state in U.S.  except for Bristol, Texarkana, Texhoma and Union City.

Conclusion:
Montana is home to the city of Missoula.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to rank solvers. Problem: natural language premises about cities and states. Need to determine if conclusion logically follows. This is entailment checking with categorical statements, universal/existential quantifiers. VAMPIRE is best for entailment. Clingo could also handle but it's more for combinatorial search. Z3 is for numeric constraints. So ranking: VAMPIRE > CLINGO > Z3.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}


### TOKEN USAGE

  Input tokens:  1,367
  Output tokens: 116
  Total tokens:  1,483

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

```
