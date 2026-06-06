# Benchmark Report (SELECTOR): FOLIO - story_184_ex_22

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 2.14s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
"Stranger Things" is a popular Netflix show.
If a Netflix show is popular, Karen will binge-watch it.
If and only if Karen binge-watches a Netflix show, she will download it.
Karen does not download "Black Mirror."
"Black Mirror" is a Netflix show.
If Karen binge-watches a Netflix show, she will share it with Lisa.

Conclusion:
Karen will share "Stranger Things" with Lisa.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to rank solvers. Problem: entailment checking from premises to conclusion. It's a natural-language logical entailment with quantifiers? Premises: "Stranger Things" is a popular Netflix show. If a Netflix show is popular, Karen will binge-watch it. If and only if Karen binge-watches a Netflix show, she will download it. Karen does not download "Black Mirror." "Black Mirror" is a Netflix show. If Karen binge-watches a Netflix show, she will share it with Lisa. Conclusion: Karen will share "Stranger Things" with Lisa. We need to determine if conclusion is true, false, or uncertain. This is a typical entailment problem. VAMPIRE is best for entailment. CLINGO is for combinatorial search, not needed. Z3 is for constraint satisfaction with numeric bounds, not needed. So ranking: VAMPIRE > CLINGO > Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}


### TOKEN USAGE

  Input tokens:  1,340
  Output tokens: 223
  Total tokens:  1,563

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

```
