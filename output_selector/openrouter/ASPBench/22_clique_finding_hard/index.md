# Benchmark Report (SELECTOR): ASPBench - 22_clique_finding_hard

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 7.61s


 SELECTOR META EVALUATOR AGENT

 Query: # Problem Statement

Given an undirected graph where each vertex has a specific **type** and **weight**, find the largest possible clique that satisfies two additional constraints: **type diversity** (no more than 2 vertices of any single type) and **weight limit** (total weight ≤ 100).

## Instance Data

**Graph:** 20 vertices (0-19) with the following properties:

| Vertex | Type | Weight |
|--------|------|--------|
| 0 | alpha | 20 |
| 1 | alpha | 20 |
| 2 | alpha | 15 |
| 3 | alpha | 20 |
| 4 | beta | 30 |
| 5 | alpha | 15 |
| 6 | beta | 30 |
| 7 | beta | 30 |
| 8 | beta | 18 |
| 9 | delta | 10 |
| 10 | delta | 10 |
| 11 | beta | 12 |
| 12 | gamma | 25 |
| 13 | gamma | 25 |
| 14 | gamma | 20 |
| 15 | delta | 5 |
| 16 | delta | 5 |
| 17 | gamma | 19 |
| 18 | alpha | 40 |
| 19 | beta | 40 |

**Edges (undirected):**
```
(0,1), (0,3), (0,4), (0,6), (0,7), (0,9), (0,10),
(1,3), (1,4), (1,6), (1,7), (1,9),
(2,5), (2,8), (2,11), (2,14), (2,17), (2,18),
(3,4), (3,6), (3,7), (3,9),
(4,6), (4,7), (4,9),
(5,8), (5,11), (5,14), (5,17), (5,19),
(6,7), (6,9),
(7,9),
(8,11), (8,14), (8,17),
(11,14), (11,17),
(12,13),
(14,17),
(15,16)
```

## Constraints

1. **Clique Property**: For any two vertices u, v in the solution clique, the edge (u, v) **must** exist in the graph.
2. **Type Diversity Constraint**: For any given type, the number of vertices of that type in the clique **must** be at most 2.
3. **Weight Limit Constraint**: The sum of weights of **all** vertices in the clique **must** be at most 100.

## Objective

Find the **maximum-sized clique** that satisfies all constraints.

**Expected optimal clique size: 6**

### Field Descriptions

- `clique`: List of vertex IDs in the clique (sorted)
- `clique_size`: Number of vertices in the clique
- `clique_edges`: List of all edges within the clique (sorted pairs)
- `clique_total_weight`: Sum of weights of all vertices in the clique
- `clique_type_distribution`: Count of vertices by type in the clique


### Thinking

- We need to rank solvers for this problem. The problem: find maximum clique with additional constraints (type diversity, weight limit). This is a combinatorial optimization / constraint satisfaction problem with numeric weight sum bound and cardinality constraints per type. It involves graph structure, clique condition (pairwise adjacency). This is typical for SAT/SMT or ASP. Z3 (SMT) can handle integer variables, constraints, and maximize size (though optimization). CLINGO (ASP) is also suitable: can generate subsets, enforce pairwise adjacency, cardinality per type, weight sum bound, and maximize size using #maximize. VAMPIRE is for first-order logic entailment, not suitable. So ranking: most suitable: CLINGO (ASP) or Z3? Both can handle, but CLINGO is more natural for combinatorial search with closed-world assumption and constraints, especially clique enumeration. Z3 can also do but may need optimization; still suitable. VAMPIRE least. Which is more suitable? Probably CLINGO is best for combinatorial search with constraints, especially clique. Z3 is second. VAMPIRE last. So output ranking: ["CLINGO", "Z3", "VAMPIRE"].
- Check if any nuance: The problem includes numeric weight limit (≤100) and type count ≤2. Both CLINGO and Z3 can handle numeric constraints. CLINGO uses aggregates (#sum) and #count, good. Z3 can handle integer arithmetic. For maximum clique, need optimization; Z3 has Optimize. Both fine. But CLINGO is more natural for combinatorial enumeration. So ranking as above.
- Thus final JSON.


{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  1,927
  Output tokens: 372
  Total tokens:  2,299

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}
```
