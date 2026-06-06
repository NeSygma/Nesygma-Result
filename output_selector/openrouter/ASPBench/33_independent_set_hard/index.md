# Benchmark Report (SELECTOR): ASPBench - 33_independent_set_hard

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 7.32s


 SELECTOR META EVALUATOR AGENT

 Query: # Problem Statement

Find the maximum independent set in a graph where vertices have attributes and must satisfy additional constraints. An independent set is a set of vertices with no edges between them. Each vertex has a **type** ('core', 'support', or 'peripheral') and a **zone** (1, 2, or 3).

## Instance Data

**Vertices:** 1 through 24

**Zones:**
- Zone 1: vertices 1-8
- Zone 2: vertices 9-16
- Zone 3: vertices 17-24

**Types:**
- Core vertices: 1, 9, 17
- Support vertices: 2, 3, 10, 11, 18, 19
- Peripheral vertices: 4, 5, 6, 7, 8, 12, 13, 14, 15, 16, 20, 21, 22, 23, 24

**Edges:**
(1,2), (1,4), (1,10), (1,17), (2,5), (2,9), (3,6), (4,7), (5,8), (6,7), (8,16), (8,24), (9,10), (9,12), (9,17), (10,14), (11,15), (12,16), (13,14), (16,24), (17,18), (17,20), (18,19), (18,21), (19,22), (20,23), (21,24)

## Constraints

1. **Standard Independence:** No two vertices in the set can be connected by an edge.
2. **Core Count Limit:** The set can contain **at most** two core vertices.
3. **Core-Support Dependency:** For every core vertex included in the set, **at least** one support vertex from the **same zone** must also be included.
4. **Conditional Zone Exclusion:** If the set contains any peripheral vertex from zone 1, then it **cannot** contain any vertex from zone 3.
5. **Peripheral Headcount Rule:** The total number of peripheral vertices in the set **must not exceed** the total number of core vertices in the set.

## Objective

Find a solution that **maximizes** the size of the independent set.

**Expected maximum size: 7**

### Field Descriptions

- `independent_set`: Array of vertex numbers in the independent set (sorted)
- `size`: Total number of vertices in the set
- `core_vertices`: Array of core vertices in the set (sorted)
- `support_vertices`: Array of support vertices in the set (sorted)
- `peripheral_vertices`: Array of peripheral vertices in the set (sorted)
- `core_count`: Number of core vertices in the set
- `support_count`: Number of support vertices in the set
- `peripheral_count`: Number of peripheral vertices in the set


### Thinking

- We need to rank solvers for this problem. The problem: find maximum independent set with additional constraints: vertex attributes (type, zone), constraints like count limits, dependencies, conditional exclusion, cardinality comparisons. This is a combinatorial optimization / constraint satisfaction problem with numeric constraints (counts, at most, at least, conditional). It involves selecting a subset of vertices maximizing size under constraints. This is typical for SAT/SMT or ASP. Z3 (SMT) handles cardinality constraints, optimization (maximizing size). CLINGO (ASP) also handles such combinatorial search with constraints, closed-world, can maximize via #maximize. VAMPIRE is for entailment, not suitable.
- Thus ranking: Most suitable: Z3 or CLINGO? Both can handle. Which is more suitable? The problem includes cardinality constraints and optimization. Z3 can do optimization with MaxSMT, but CLINGO is also good for combinatorial optimization with #maximize. However, the problem includes conditional zone exclusion (if peripheral in zone1 then no vertex from zone3). That's a logical implication, both can handle. The graph independence is a pairwise constraint (no edge both selected). That's a typical SAT constraint.
- Given the problem is essentially a CSP with optimization, both Z3 and CLINGO are suitable. Which is more appropriate? Since there are numeric counting constraints (peripheral count <= core count, at most two core vertices, at least one support per core in same zone). Z3 handles arithmetic constraints naturally. CLINGO can also handle cardinality via aggregates (#count). But Z3 is perhaps more straightforward for numeric constraints and optimization. So ranking: Z3 most suitable, CLINGO second, VAMPIRE least.
- Thus output JSON.


{
    "solver_ranking": ["Z3", "CLINGO", "VAMPIRE"]
}

### TOKEN USAGE

  Input tokens:  1,865
  Output tokens: 390
  Total tokens:  2,255

COMPLETE

## Selector Final Answer

```json
{
    "solver_ranking": ["Z3", "CLINGO", "VAMPIRE"]
}
```
