# Benchmark Report (SELECTOR): FOLIO - story_120_ex_70

**Provider:** nvidia
**Model:** nvidia/nemotron-3-nano-30b-a3b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: high
**Duration:** 25.82s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Badults is a British Sitcom series starring members of Pappy's.
Badults was piloted in July 2013 on BBC Three.
The Working title "The Secret Dude Society" was used for Badults.
Andrew Collins was the script editor for Badults.

Conclusion:
No members of Pappy's have starred in a show piloting on BBC Two or BBC Three.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to analyze problem type and structure, then rank solvers from most suitable to least suitable. No solving. Provide JSON ranking.
- Problem: Premises about Badults, a British sitcom starring members of Pappy's, piloted in July 2013 on BBC Three, working title etc., script editor. Conclusion: "No members of Pappy's have starred in a show piloting on BBC Two or BBC Three."
- We need to determine entailment: Does conclusion follow? It's a negative universal claim about members of Pappy's starring in a show piloting on BBC Two or BBC Three. Premises mention that Badults (which stars members of Pappy's) was piloted on BBC Three. That is a show piloted on BBC Three, starring members of Pappy's. So there exists at least one member of Pappy's who starred in a show piloting on BBC Three (namely Badults). Therefore the conclusion "No members of Pappy's have starred in a show piloting on BBC Two or BBC Three" is false (contradicted). But the question is about entailment classification: True/False/Uncertain. The conclusion is actually false given premises. But the task is to rank solvers based on suitability.
- We need to analyze problem type: It's a logical entailment with universal negative conclusion, involving categorical statements, quantifiers, and possibly negation. It's about determining truth of conclusion given premises. This matches VAMPIRE's strength: determining whether a natural-language conclusion logically follows from premises, True/False/Uncertain, using universal/existential quantifiers, etc. So VAMPIRE is most suitable.
- Clingo is for combinatorial search, planning, etc. Not needed. Z3 is for constraints with numeric, positional, etc. Not needed. So ranking: VAMPIRE most suitable, then maybe Z3 or Clingo? Which is second? The problem is purely logical entailment, no numeric or positional constraints. Z3 could handle but not ideal; Clingo also could encode but not ideal. Which is more suitable? Probably Z3 is more general for SAT/SMT but this is simple logical reasoning; VAMPIRE is specialized for such tasks. So second could be Z3, third Clingo. Or maybe Clingo could also handle but less direct. I'd rank: VAMPIRE > Z3 > CLINGO. Provide JSON.
- Thus output:
- { "solver_ranking": ["VAMPIRE", "Z3", "CLINGO"] }


{
    "solver_ranking": ["VAMPIRE", "Z3", "CLINGO"]
}

### TOKEN USAGE

  Input tokens:  1,299
  Output tokens: 556
  Total tokens:  1,855

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "Z3", "CLINGO"]
}
```
