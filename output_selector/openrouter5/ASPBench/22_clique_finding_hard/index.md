# Benchmark Report (SELECTOR): ASPBench - 22_clique_finding_hard

**Provider:** openrouter5
**Model:** deepseek/deepseek-v4-flash
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 7.18s


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

This problem is a **combinatorial optimization** task over a discrete graph with explicit numeric constraints (weight ≤ 100) and cardinality constraints (≤ 2 per type).  

- The **clique property** requires checking pairwise edges, which is a classic constraint satisfaction / search problem.  
- The **type diversity** constraint is a simple cardinality bound per category.  
- The **weight limit** is a numeric sum constraint with a fixed bound.  

These features — discrete search, numeric bounds, and constraint satisfaction — are exactly what **Clingo** (Answer Set Programming) handles well with its generate-define-test paradigm and built-in optimization (`#maximize`).  

**Z3** could also solve this using integer variables and constraints, but it is less natural for graph clique enumeration than Clingo’s rule-based approach.  

**VAMPIRE** is unsuitable because it is designed for first-order logic entailment, not for numeric optimization or combinatorial search over a finite graph with weight constraints.  

Thus the ranking is:  

```json
{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}
```

### TOKEN USAGE

  Input tokens:  1,872
  Output tokens: 242
  Total tokens:  2,114

COMPLETE

## Selector Final Answer

```json
This problem is a **combinatorial optimization** task over a discrete graph with explicit numeric constraints (weight ≤ 100) and cardinality constraints (≤ 2 per type).  

- The **clique property** requires checking pairwise edges, which is a classic constraint satisfaction / search problem.  
- The **type diversity** constraint is a simple cardinality bound per category.  
- The **weight limit** is a numeric sum constraint with a fixed bound.  

These features — discrete search, numeric bounds, and constraint satisfaction — are exactly what **Clingo** (Answer Set Programming) handles well with its generate-define-test paradigm and built-in optimization (`#maximize`).  

**Z3** could also solve this using integer variables and constraints, but it is less natural for graph clique enumeration than Clingo’s rule-based approach.  

**VAMPIRE** is unsuitable because it is designed for first-order logic entailment, not for numeric optimization or combinatorial search over a finite graph with weight constraints.  

Thus the ranking is:  

```json
{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}
```
```
