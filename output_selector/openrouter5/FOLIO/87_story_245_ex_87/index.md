# Benchmark Report (SELECTOR): FOLIO - story_245_ex_87

**Provider:** openrouter5
**Model:** deepseek/deepseek-v4-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 1.54s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
In superhero movies, the good guys always win.
The Surprising Adventures of Sir Digby Chicken Caesar is a superhero movie.
Good guys fight bad guys and vice versa.
Sir Digby fights his nemesis.
If a superhero movie is named after a character, that character is a good guy.
The Surprising Adventures of Sir Digby Chicken Caesar is named after Sir Digby.
If somebody wins a fight, the person they are fighting does not win.
If a superhero movie is named after a character, that character is in the movie.

Conclusion:
Sir Digby’s nemesis does not win.

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,309
  Output tokens: 24
  Total tokens:  1,333

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
