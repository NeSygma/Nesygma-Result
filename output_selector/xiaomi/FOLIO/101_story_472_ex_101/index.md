# Benchmark Report (SELECTOR): FOLIO - story_472_ex_101

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 2.83s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
Animals are either invertebrates or vertebrates.
All animals with backbones reproduce by male-and-female mating. 
All vertebrate animals have a backbone.
All bees do not reproduce by male-and-female mating.
All queen bees are bees.
Harry is a bee.

Conclusion:
If Harry is either both a vertebrate and an animal with a backbone, or neither a vertebrate nor an animal with a backbone, then Harry is neither an invertebrate nor a queen bee.

Is the conclusion True, False, or Uncertain?

{
    "solver_ranking": ["VAMPIRE", "Z3", "CLINGO"]
}

### TOKEN USAGE

  Input tokens:  1,296
  Output tokens: 24
  Total tokens:  1,320

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "Z3", "CLINGO"]
}
```
