# Benchmark Report (SELECTOR): FOLIO - story_120_ex_70

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 3.79s


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

- We need to analyze the problem type and structure to rank solvers. The problem: Premises are facts about a sitcom. Conclusion: "No members of Pappy's have starred in a show piloting on BBC Two or BBC Three." We need to determine if conclusion is true, false, or uncertain. This is a logical entailment problem: given premises, does the conclusion logically follow? It's a first-order logic entailment with quantifiers? The conclusion is a universal statement: For all members of Pappy's, they have not starred in a show piloting on BBC Two or BBC Three. The premises mention that Badults is a British Sitcom starring members of Pappy's, and that Badults was piloted in July 2013 on BBC Three. So we have a counterexample: members of Pappy's starred in a show piloting on BBC Three. So the conclusion is false. This is a simple entailment check. So VAMPIRE is best. Clingo could also handle but it's more for combinatorial search. Z3 is for constraints, not needed. So ranking: VAMPIRE > CLINGO > Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}


### TOKEN USAGE

  Input tokens:  1,329
  Output tokens: 269
  Total tokens:  1,598

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

```
