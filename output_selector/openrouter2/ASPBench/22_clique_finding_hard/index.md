# Benchmark Report (SELECTOR): ASPBench - 22_clique_finding_hard

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 4.41s


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

- We need to rank solvers: VAMPIRE, CLINGO, Z3. Problem: find maximum clique with constraints: type diversity (max 2 per type) and weight limit <=100. Graph with 20 vertices. This is a combinatorial optimization problem: find largest clique under constraints. We need to find maximum size clique. This is a constraint satisfaction / optimization problem. We can encode as SAT/SMT or as ASP. Which solver best? Let's analyze.
- VAMPIRE: first-order logic theorem prover. It can handle quantifiers, but not optimization. It can prove existence of a clique of size k? We could encode as a formula: there exist k vertices such that all pairwise edges exist, type constraints, weight sum <=100. But to find maximum size, we would need to test each k. Could be done but not efficient. But VAMPIRE is not designed for optimization or numeric constraints. It can handle arithmetic? It can handle equality, but not integer arithmetic? It can handle arithmetic via built-in functions? Not sure. But weight sum <=100 is numeric. Might be possible but not ideal. So VAMPIRE is least suitable.
- CLINGO: ASP is good for combinatorial search, constraints, cardinality, optimization. We can encode vertices as atoms, constraints as rules, cardinality constraints for type diversity, weight sum <=100. We can use #maximize to maximize clique size. ASP is good for this. So CLINGO is suitable.
- Z3: SMT solver can handle integer variables, constraints, cardinality, optimization. We can encode each vertex as a boolean variable indicating inclusion. Constraints: for each pair not connected, at least one of them false. Type constraints: sum of booleans for each type <=2. Weight sum <=100. Maximize sum of booleans. This is a classic SAT/SMT optimization. Z3 can handle this well. So Z3 is also suitable. Which is more suitable? Both can solve. But the problem is small (20 vertices). Z3 is straightforward. ASP also works. Which is more natural? The problem is a combinatorial optimization with constraints. Z3 is a general solver for such constraints. CLINGO is specialized for combinatorial search. Both are good. But ranking: maybe Z3 is best because it can handle numeric constraints easily and optimization. CLINGO is also good but might need more encoding. VAMPIRE is least.
- Thus ranking: Z3 > CLINGO > VAMPIRE. Provide JSON.


{
    "solver_ranking": ["Z3", "CLINGO", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  1,935
  Output tokens: 550
  Total tokens:  2,485

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["Z3", "CLINGO", "VAMPIRE"]
}
```
