# Benchmark Report (SELECTOR): FOLIO - story_456_ex_191

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 3.55s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Some professional basketball players are not American nationals.
All professional basketball players can do jump shots.
If someone can jump shots, they leap straight into the air.
If someone leaps straight into the air, they activate their leg muscles. 
Yuri does not activate his leg muscles.

Conclusion:
If Yuri does not leap straight into the air, then Yuri is an American professional basketball player.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to analyze the problem type and structure, and rank solvers. The problem: Premises are a set of categorical statements with quantifiers, and a conclusion that is a conditional statement. We need to determine if the conclusion is true, false, or uncertain. This is a typical entailment checking problem: given premises, does the conclusion logically follow? The conclusion is a conditional: "If Yuri does not leap straight into the air, then Yuri is an American professional basketball player." We need to see if this is entailed, contradicted, or uncertain. This is a first-order logic entailment problem with quantifiers, predicates, and a specific individual. The solver that best fits is VAMPIRE, which is for first-order logic entailment. CLINGO is for combinatorial search, not needed. Z3 is for constraint satisfaction with numeric bounds, not needed. So ranking: VAMPIRE > CLINGO > Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}


### TOKEN USAGE

  Input tokens:  1,329
  Output tokens: 227
  Total tokens:  1,556

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

```
