# Benchmark Report (SELECTOR): FOLIO - story_245_ex_87

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 3.49s


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


### Thinking

- We need to rank solvers: VAMPIRE, CLINGO, Z3. The problem: It's a logical entailment problem: premises about good guys, superhero movies, etc. We need to determine if conclusion follows. This is a typical entailment checking with universal/existential quantifiers, predicates, etc. So VAMPIRE is best. CLINGO could also handle but it's more for combinatorial search. Z3 is for numeric constraints. So ranking: VAMPIRE > CLINGO > Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,373
  Output tokens: 142
  Total tokens:  1,515

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
