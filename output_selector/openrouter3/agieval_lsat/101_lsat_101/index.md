# Benchmark Report (SELECTOR): agieval_lsat - lsat_101

**Provider:** openrouter3
**Model:** xiaomi/mimo-v2-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 2.16s


 SELECTOR META EVALUATOR AGENT

 Query: Exactly five witnesses—Franco, Garcia, Hong, Iturbe, and Jackson—are to be scheduled to testify at a hearing that is to take exactly three days of one week—Monday, Tuesday, and Wednesday. Each witness testifies on exactly one day of the hearing. The schedule must meet the following conditions: Franco does not testify on the same day that Garcia testifies. Iturbe testifies on Wednesday. Exactly two witnesses testify on Tuesday. Hong does not testify on Monday. At least one witness testifies on Monday.Q: If Jackson is the only witness scheduled to testify on Monday, which one of the following must be true of the schedule? Answer Choices: (A)Franco is scheduled to testify on Wednesday. (B)Hong is scheduled to testify on Tuesday. (C)Garcia is scheduled to testify on Tuesday. (D)Franco is scheduled to testify on the same day as Hong. (E)Garcia is scheduled to testify on the same day as Hong.
A: Among A through E, the answer is

{
    "solver_ranking": ["Z3", "CLINGO", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  1,400
  Output tokens: 24
  Total tokens:  1,424

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["Z3", "CLINGO", "VAMPIRE"]
}
```
