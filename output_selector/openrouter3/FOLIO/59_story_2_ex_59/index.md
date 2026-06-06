# Benchmark Report (SELECTOR): FOLIO - story_2_ex_59

**Provider:** openrouter3
**Model:** xiaomi/mimo-v2-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 2.40s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Billings is a city in the state of Montana in U.S.
The state of Montana includes the cities of Butte, Helena, and Missoula.
White Sulphur Springs and Butte are cities in the same state in U.S.
The city of St Pierre is not in the state of Montana.
Any city in Butte is not in St Pierre.
A city can only be in one state in U.S.  except for Bristol, Texarkana, Texhoma and Union City.

Conclusion:
St Pierre and Bismarck are in the same state.

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,315
  Output tokens: 24
  Total tokens:  1,339

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
