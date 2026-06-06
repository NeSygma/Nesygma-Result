# Benchmark Report (SELECTOR): ASPBench - 22_clique_finding_easy

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 5.21s


 SELECTOR META EVALUATOR AGENT

 Query: # Problem Statement

Given an undirected graph, find the largest clique where every pair of vertices is connected by an edge.

## Instance Data

**Vertices:** {0, 1, 2, 3, 4, 5, 6}

**Edges:**
- (0, 1), (0, 2), (0, 3)
- (1, 2), (1, 3), (1, 4)
- (2, 3), (2, 5)
- (3, 4), (3, 5)
- (4, 5), (4, 6)
- (5, 6)

## Constraints

1. **All vertices** in the clique must be pairwise connected
2. For any two vertices u, v in the clique, edge (u, v) **must exist** in the graph

## Objective

Find a solution that **maximizes** the clique size.

**Expected optimal clique size:** 4

**Notes:**
- For a clique of size k, there should be k(k-1)/2 edges in clique_edges
- Multiple optimal solutions may exist with the same clique_size


### Thinking

- We need to rank solvers for this problem. The problem: find largest clique in an undirected graph, maximize size. This is a combinatorial optimization / search problem, with constraints about pairwise edges. This is typical for answer set programming (CLINGO) or SAT/SMT (Z3). VAMPIRE is for first-order logic entailment, not suitable. Between CLINGO and Z3: CLINGO is good for combinatorial search, closed-world, generate candidate cliques, constraints. Z3 can also handle via integer variables and constraints, but may be less natural for combinatorial enumeration; however it can handle cardinality constraints and adjacency matrix. Both are possible. Which is most suitable? Probably CLINGO because it's a classic NP-complete combinatorial problem, ASP is good for maximal clique. Z3 also works but may be less straightforward due to need to encode adjacency constraints and maximize cardinality; but Z3 supports optimization. However the problem is small, but general. The ranking: CLINGO most suitable, Z3 second, VAMPIRE least.


{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  1,480
  Output tokens: 254
  Total tokens:  1,734

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}
```
