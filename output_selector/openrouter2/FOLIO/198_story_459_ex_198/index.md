# Benchmark Report (SELECTOR): FOLIO - story_459_ex_198

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 2.06s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Jane does not like any animals that bark.
All dogs are animals that bark.
Jane likes all animals that jump.
If an animal has legs, then it jumps.
If an animal is terricolous, then it has legs. 
KiKi is an animal.
If KiKi neither jumps nor has legs, then KiKi is terricolous or has legs.

Conclusion:
KiKi does not bark and he is not a dog.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to analyze the problem type and structure to rank solvers. The problem: premises with universal statements, existential? We have a conclusion about KiKi. It's a logical entailment problem: determine if conclusion follows from premises. This is a typical first-order logic entailment. VAMPIRE is best for entailment checking. Clingo is for combinatorial search, not needed. Z3 is for constraint satisfaction with numeric bounds, not needed. So ranking: VAMPIRE > CLINGO > Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}


### TOKEN USAGE

  Input tokens:  1,340
  Output tokens: 139
  Total tokens:  1,479

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

```
