# Benchmark Report (SELECTOR): FOLIO - story_232_ex_26

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 1.54s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Beijing is the capital of the People's Republic of China. 
Beijing is the capital city of the world's most populous nation.
Beijing is located in Northern China.
Beijing hosted the 2008 Summer Olympics and 2008 Summer Paralympics Games.
Beijing has hosted the Summer and Winter Olympics and the Summer and Winter Paralympics.
Many of Beijing's 91 universities consistently rank among the best universities in the world.

Conclusion:
Beijing is located in southern China.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to rank solvers. The problem: premises about Beijing, conclusion about location. It's a simple entailment check: does conclusion logically follow? It's a factual knowledge question. The solver type: VAMPIRE is for entailment checking. CLINGO is for combinatorial search. Z3 is for constraint satisfaction. So VAMPIRE is best. CLINGO second? But CLINGO is for combinatorial search, not needed. Z3 is least. So ranking: VAMPIRE, CLINGO, Z3.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,351
  Output tokens: 141
  Total tokens:  1,492

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
