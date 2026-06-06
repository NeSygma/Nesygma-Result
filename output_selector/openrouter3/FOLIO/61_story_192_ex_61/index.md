# Benchmark Report (SELECTOR): FOLIO - story_192_ex_61

**Provider:** openrouter3
**Model:** xiaomi/mimo-v2-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 1.49s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
International students in the US have either an F1 visa or a J1 visa.
An international student in the US with an F1 visa needs to apply for CPT or OPT if the student wants to work in the US.
Mike is an international student.
Mike needs to apply for CPT if he wants to work in the US.

Conclusion:
Mike has an F1 visa.

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,275
  Output tokens: 24
  Total tokens:  1,299

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
