# Benchmark Report (SELECTOR): ASPBench - 28_graph_isomorphism_easy

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 8.57s


 SELECTOR META EVALUATOR AGENT

 Query: # Problem Statement

Determine if two given graphs are isomorphic by finding a bijection between their vertices that preserves adjacency relationships.

## Instance Data

**Graph 1 (G1)**

Vertices: 0, 1, 2, 3, 4

Edges:
- (0, 1)
- (0, 2)
- (1, 3)
- (2, 4)
- (3, 4)

**Graph 2 (G2)**

Vertices: a, b, c, d, e

Edges:
- (a, b)
- (a, c)
- (b, d)
- (c, e)
- (d, e)

## Constraints

1. **Bijection**: There must exist a bijection f: V1 → V2 mapping G1 vertices to G2 vertices
2. **Adjacency preservation**: For **all** edges (u,v) in G1, the mapped edge (f(u),f(v)) **must** exist in G2
3. **Reverse preservation**: For **all** edges in G2, there **must** be a corresponding edge in G1
4. **Degree preservation**: Vertex degrees **must** be preserved under the mapping

## Objective

Determine if the graphs are isomorphic and find the vertex mapping if one exists.

**Field descriptions:**
- `is_isomorphic` (boolean): Whether the graphs are isomorphic
- `mapping` (object or null): Vertex mapping from G1 to G2 as strings (null if not isomorphic)
- `preserved_edges` (array): Edge correspondence pairs as [["u,v", "f(u),f(v)"], ...] (empty if not isomorphic)


### Thinking

- We need to rank solvers for this problem: graph isomorphism, find bijection preserving adjacency. This is a combinatorial search / constraint satisfaction problem with discrete entities (vertices) and adjacency constraints. It is essentially a CSP: assign each vertex of G1 to a vertex of G2, bijection, adjacency constraints. This is typical for SAT/SMT or ASP. Which solver is most suitable? Let's consider each:
- VAMPIRE: First-order logic theorem proving, open-world, not good for numeric counting or explicit bijection search. Could encode as logical entailment but not ideal.
- CLINGO: ASP, good for combinatorial search, closed-world, can encode bijection, adjacency constraints, find mapping. Very suitable.
- Z3: SMT solver, can handle integer variables representing mapping, constraints for bijection (Distinct), adjacency constraints as logical formulas. Also suitable. Which is more suitable? Graph isomorphism is a classic CSP; both ASP and SMT can solve. However, Z3 handles arithmetic and distinct constraints well, but the problem is purely combinatorial with no arithmetic beyond distinctness. ASP is often used for graph isomorphism. Z3 can also do it but may need encoding of adjacency as boolean constraints. Both are okay. Which is most suitable? Probably CLINGO because it's a pure combinatorial search with closed-world, and graph isomorphism is typical for ASP. Z3 is also okay but maybe second. VAMPIRE least.
- Thus ranking: CLINGO > Z3 > VAMPIRE.
- Return JSON.


{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  1,594
  Output tokens: 348
  Total tokens:  1,942

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["CLINGO", "Z3", "VAMPIRE"]
}
```
