# Benchmark Report (SELECTOR): ASPBench - 22_clique_finding_hard

**Provider:** google
**Model:** gemini-3.1-flash-lite-preview
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 7.40s


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

- **Defining the Problem**
- I'm focusing on defining the largest clique problem in an undirected graph, emphasizing the constraint that all vertices within the clique must be interconnected. I'm also considering the constraint of maximizing the diversity or type of members of the clique.
- **Evaluating Solution Approaches**
- I've been evaluating CLINGO and Z3. I'm leaning toward CLINGO due to its superior combinatorial search capabilities, especially given the "all pairs connected" constraint of a clique. The constraints for type diversity and weight limit seem straightforward to implement. My initial assessment indicates CLINGO's strong suitability for optimizing clique size.
- **Refining Constraint Formulation**
- I'm now refining the constraint formulation for the clique problem, including both weight and type diversity constraints within CLINGO's framework. I'm focusing on the translation of these constraints into CLINGO's syntax to ensure a precise and efficient representation. The constraint syntax for CLINGO appears concise and efficient. Both CLINGO and Z3 are highly suitable, but CLINGO's syntax leans more cleanly toward graph-based problems. I've begun to formulate the problem in CLINGO's concise format.


The problem is a combinatorial optimization problem that requires finding the largest subset of vertices (a clique) that satisfies specific relational (clique property), categorical (type diversity), and arithmetic (weight limit) constraints.

1. **CLINGO (Answer Set Programming)**: This is the most suitable solver. ASP is designed specifically for combinatorial search problems where you need to find a valid configuration that satisfies a set of logical rules and constraints. It handles the "clique" constraint (all pairs must be connected) and the "type diversity" constraint (count per type) very naturally using integrity constraints and aggregate functions. Maximizing the clique size is a native feature of Clingo using the `#maximize` directive.

2. **Z3 (SMT Solver)**: Z3 is the second choice. It is highly effective at handling the arithmetic constraints (sum of weights ≤ 100) and boolean constraints (clique property). It can model the problem using boolean variables for each vertex and use optimization modules to find the maximum size. While it is very capable, the syntax for graph-based combinatorial search is often slightly more verbose than Clingo's declarative approach.

3. **VAMPIRE (Automated Theorem Prover)**: VAMPIRE is the least suitable. It is designed for first-order logic entailment and proving theorems, not for finding optimal configurations or solving combinatorial search problems. While it could theoretically verify if a specific set is a clique, it is not designed to search for the largest such set under numeric constraints.

{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  1,972
  Output tokens: 1,344
  Total tokens:  3,316

COMPLETE

## Selector Final Answer

```json
The problem is a combinatorial optimization problem that requires finding the largest subset of vertices (a clique) that satisfies specific relational (clique property), categorical (type diversity), and arithmetic (weight limit) constraints.

1. **CLINGO (Answer Set Programming)**: This is the most suitable solver. ASP is designed specifically for combinatorial search problems where you need to find a valid configuration that satisfies a set of logical rules and constraints. It handles the "clique" constraint (all pairs must be connected) and the "type diversity" constraint (count per type) very naturally using integrity constraints and aggregate functions. Maximizing the clique size is a native feature of Clingo using the `#maximize` directive.

2. **Z3 (SMT Solver)**: Z3 is the second choice. It is highly effective at handling the arithmetic constraints (sum of weights ≤ 100) and boolean constraints (clique property). It can model the problem using boolean variables for each vertex and use optimization modules to find the maximum size. While it is very capable, the syntax for graph-based combinatorial search is often slightly more verbose than Clingo's declarative approach.

3. **VAMPIRE (Automated Theorem Prover)**: VAMPIRE is the least suitable. It is designed for first-order logic entailment and proving theorems, not for finding optimal configurations or solving combinatorial search problems. While it could theoretically verify if a specific set is a clique, it is not designed to search for the largest such set under numeric constraints.

{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}
```
