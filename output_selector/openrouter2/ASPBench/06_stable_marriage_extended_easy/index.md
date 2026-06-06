# Benchmark Report (SELECTOR): ASPBench - 06_stable_marriage_extended_easy

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 2.10s


 SELECTOR META EVALUATOR AGENT

 Query: # Problem Statement

Find all stable marriages between 4 men and 4 women where each person has preference rankings over acceptable partners. A stable marriage is one where no two people would prefer to be matched with each other over their current partners.

## Instance Data

**Men and Women:**
- Men: m1, m2, m3, m4
- Women: w1, w2, w3, w4

**Men's Preferences** (in order of decreasing preference, unacceptable partners not listed):
- m1: w1, w2, w3
- m2: w2, w3, w4
- m3: w3, w4, w1
- m4: w4, w1, w2

**Women's Preferences** (in order of decreasing preference, unacceptable partners not listed):
- w1: m4, m1, m3
- w2: m1, m2, m4
- w3: m2, m3, m1
- w4: m3, m4, m2

## Constraints

1. **Matching**: Each person can be matched to **at most one** partner
2. **Acceptability**: Only pairs where **both** people find each other acceptable can be matched
3. **Stability**: **No** blocking pair should exist - a blocking pair is two people who:
   - Are not currently matched to each other
   - Both find each other acceptable
   - Both would prefer each other over their current partner (or being unmatched)

## Objective

Find **all** stable matchings (there are multiple solutions).

- `stable_matchings`: Array of all stable matchings, where each matching is an array of pairs `["man", "woman"]`
- `count`: Total number of stable matchings found


### Thinking

- We need to rank solvers: VAMPIRE, CLINGO, Z3. Problem: find all stable marriages between 4 men and 4 women with preferences. This is a combinatorial search problem: find all stable matchings. We need to enumerate all solutions. This is a typical stable marriage enumeration problem. We need to find all stable matchings. This is a combinatorial search with constraints: each man matched to at most one woman, each woman matched to at most one man, acceptability constraints, stability constraints. We need to output all matchings. This is a constraint satisfaction problem with combinatorial enumeration. The solver that best fits: CLINGO (Answer Set Programming) is good for combinatorial search, enumeration of all solutions. Z3 can also solve but enumeration of all solutions might be more complex; but Z3 can find models but enumerating all might require additional logic. VAMPIRE is for theorem proving, not enumeration. So ranking: CLINGO > Z3 > VAMPIRE. Provide JSON.


{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}


### TOKEN USAGE

  Input tokens:  1,622
  Output tokens: 243
  Total tokens:  1,865

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}

```
