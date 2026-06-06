# Benchmark Report (SELECTOR): FOLIO - story_120_ex_70

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 11.26s


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

- We need to decide which solver is most suitable for this problem. The problem: given premises about Badults (British sitcom starring members of Pappy's, piloted in July 2013 on BBC Three, working title, script editor). Conclusion: "No members of Pappy's have starred in a show piloting on BBC Two or BBC Three." We need to answer True/False/Uncertain.
- This is a logical entailment check: from premises, does the conclusion follow? Premises say Badults starred members of Pappy's, and Badults was piloted on BBC Three. So there exists a member of Pappy's who starred in a show piloted on BBC Three. The conclusion says no members of Pappy's have starred in a show piloting on BBC Two or BBC Three. That is contradicted by premises. So conclusion is false. But we are not to solve, just rank solvers.
- The problem is entailment with quantifiers, categorical statements, open-world? It's about checking if conclusion follows from premises. That's exactly VAMPIRE's domain: first-order logic entailment, open-world assumption. CLINGO is for combinatorial search, not needed. Z3 could encode but it's more numeric; but could also handle boolean logic but not needed. So most suitable: VAMPIRE. Second: Z3 maybe can handle but less natural. Least: CLINGO.
- Thus ranking: ["VAMPIRE","Z3","CLINGO"].
- Return JSON.


{
    "solver_ranking": ["VAMPIRE", "Z3", "CLINGO"]
}

### TOKEN USAGE

  Input tokens:  1,321
  Output tokens: 336
  Total tokens:  1,657

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "Z3", "CLINGO"]
}
```
