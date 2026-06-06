# Benchmark Report (SYSTEM1): ASPBench - 22_clique_finding_hard

**Provider:** openrouter2
**Model:** openai/gpt-oss-20b
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 3.47s


 SYSTEM 1 PURE REASONING AGENT

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

## Output Format

The solution must be a JSON object with the following structure:

```json
{
  "clique": [2, 5, 8, 11, 14, 17],
  "clique_size": 6,
  "clique_edges": [
    [2, 5], [2, 8], [2, 11], [2, 14], [2, 17],
    [5, 8], [5, 11], [5, 14], [5, 17],
    [8, 11], [8, 14], [8, 17],
    [11, 14], [11, 17],
    [14, 17]
  ],
  "clique_total_weight": 99,
  "clique_type_distribution": {
    "alpha": 2,
    "beta": 2,
    "gamma": 2
  }
}
```

### Field Descriptions

- `clique`: List of vertex IDs in the clique (sorted)
- `clique_size`: Number of vertices in the clique
- `clique_edges`: List of all edges within the clique (sorted pairs)
- `clique_total_weight`: Sum of weights of all vertices in the clique
- `clique_type_distribution`: Count of vertices by type in the clique


Return your final answer in JSON format.


### Thinking

- We need to solve the problem: find largest clique with constraints. The expected optimal clique size is 6. The example solution given: vertices [2,5,8,11,14,17] with weight 99, type distribution alpha 2, beta 2, gamma 2. We need to verify if this is indeed a clique: edges between all pairs? Let's check edges list: Provided edges include (2,5), (2,8), (2,11), (2,14), (2,17). Yes. (5,8), (5,11), (5,14), (5,17). Yes. (8,11), (8,14), (8,17). Yes. (11,14), (11,17). Yes. (14,17). Yes. So it's a clique of size 6.
- We need to confirm that no larger clique exists that satisfies constraints. The expected optimal size is 6. So we can output that clique. But we must produce JSON exactly as specified. The example output includes clique_edges sorted pairs. We need to produce same. Let's verify weight: Vertex weights: 2:15, 5:15, 8:18, 11:12, 14:20, 17:19. Sum: 15+15=30, +18=48, +12=60, +20=80, +19=99. Yes.
- Type distribution: Vertex 2 alpha, 5 alpha, 8 beta, 11 beta, 14 gamma, 17 gamma. So alpha 2, beta 2, gamma 2. Good.
- We need to output JSON with fields: clique, clique_size, clique_edges, clique_total_weight, clique_type_distribution. The clique list sorted: [2,5,8,11,14,17]. clique_edges sorted pairs: we need to list all 15 edges (since 6 choose 2 = 15). They are sorted pairs ascending? The example shows [2,5], [2,8], [2,11], [2,14], [2,17], [5,8], [5,11], [5,14], [5,17], [8,11], [8,14], [8,17], [11,14], [11,17], [14,17]. That is sorted lexicographically by first then second. Good.
- We need to output exactly that JSON. Ensure no extra whitespace? The problem says output JSON object. We can output with pretty formatting? Usually they accept any JSON. We'll output as single line or pretty. We'll output as pretty with indentation? The example shows pretty. We'll output same.
- Thus final answer: JSON object with those fields.


```json
{
  "clique": [2, 5, 8, 11, 14, 17],
  "clique_size": 6,
  "clique_edges": [
    [2, 5], [2, 8], [2, 11], [2, 14], [2, 17],
    [5, 8], [5, 11], [5, 14], [5, 17],
    [8, 11], [8, 14], [8, 17],
    [11, 14], [11, 17],
    [14, 17]
  ],
  "clique_total_weight": 99,
  "clique_type_distribution": {
    "alpha": 2,
    "beta": 2,
    "gamma": 2
  }
}
```

### TOKEN USAGE

  Input tokens:  1,015
  Output tokens: 764
  Total tokens:  1,779

COMPLETE

## System 1 Final Answer

```json
```json
{
  "clique": [2, 5, 8, 11, 14, 17],
  "clique_size": 6,
  "clique_edges": [
    [2, 5], [2, 8], [2, 11], [2, 14], [2, 17],
    [5, 8], [5, 11], [5, 14], [5, 17],
    [8, 11], [8, 14], [8, 17],
    [11, 14], [11, 17],
    [14, 17]
  ],
  "clique_total_weight": 99,
  "clique_type_distribution": {
    "alpha": 2,
    "beta": 2,
    "gamma": 2
  }
}
```
```
