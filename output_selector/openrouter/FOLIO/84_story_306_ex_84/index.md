# Benchmark Report (SELECTOR): FOLIO - story_306_ex_84

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 7.44s


 SELECTOR META EVALUATOR AGENT

 Query: Premises:
If a restaurant is listed in Yelp’s recommendations, then the restaurant has not received many negative reviews.
All restaurants with a rating greater than four are listed in Yelp’s recommendations.
Some restaurants that do not provide take-out service receive many negative reviews.
All restaurants that are popular among local residents have ratings greater than four.
The Hamden Plaza Subway store has a rating greater than four, or it is popular among local residents.

Conclusion:
If the Hamden Plaza Subway store provides take-out service and receives many negative reviews, then its rating is greater than 4 and it does not provide take-out service.

Is the conclusion True, False, or Uncertain?


### Thinking

- We need to decide which solver is most suitable. The problem: natural language premises with conditionals, universal statements, existential, disjunction. The question asks about truth of a conclusion (True/False/Uncertain) given premises. This is entailment checking with quantifiers, open-world? The premises involve universal statements ("All restaurants ..."), some existential ("Some restaurants ..."), a disjunction. The conclusion is a conditional statement about a specific entity (Hamden Plaza Subway store). This is typical for VAMPIRE (first-order logic entailment). CLINGO could encode but it's more for combinatorial search; not needed. Z3 could also encode but involves quantifiers? Z3 can handle quantifier-free but with quantifiers it's more complex; also open-world vs closed-world? The problem is about logical entailment with universal and existential quantifiers, not numeric constraints. So VAMPIRE is best. Next best maybe CLINGO? But CLINGO uses closed-world and would need to ground all possibilities; could be used but less natural. Z3 is less suitable because quantifiers and open-world reasoning are not its strength. So ranking: VAMPIRE most suitable, CLINGO second, Z3 least.
- Thus output JSON.


{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}

### TOKEN USAGE

  Input tokens:  1,365
  Output tokens: 284
  Total tokens:  1,649

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["VAMPIRE", "CLINGO", "Z3"]
}
```
