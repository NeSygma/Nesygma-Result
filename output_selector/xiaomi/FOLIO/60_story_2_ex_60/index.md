# Benchmark Report (SELECTOR): FOLIO - story_2_ex_60

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 3.13s


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

{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,314
  Output tokens: 24
  Total tokens:  1,338

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
