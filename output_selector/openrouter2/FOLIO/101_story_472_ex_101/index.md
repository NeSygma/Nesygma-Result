# Benchmark Report (SELECTOR): FOLIO - story_472_ex_101

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 3.75s


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


### Thinking

- We need to rank solvers. Problem: It's a logical entailment problem: premises about categories, quantifiers, and a conclusion about a specific individual (Harry). We need to determine if conclusion is true, false, or uncertain. This is a typical first-order logic entailment. VAMPIRE is best for entailment checking. Clingo could also handle but it's more for combinatorial search; but we could encode as facts and rules. But VAMPIRE is more natural. Z3 is for constraint satisfaction with numeric bounds; not needed. So ranking: VAMPIRE > CLINGO > Z3. Provide JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}


### TOKEN USAGE

  Input tokens:  1,350
  Output tokens: 159
  Total tokens:  1,509

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

```
