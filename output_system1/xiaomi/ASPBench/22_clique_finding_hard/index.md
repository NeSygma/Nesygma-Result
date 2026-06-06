# Benchmark Report (SYSTEM1): ASPBench - 22_clique_finding_hard

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 13.27s


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

Looking at this problem, I need to find the largest clique that satisfies type diversity (max 2 per type) and weight limit (≤100).

Let me analyze the graph structure:

**Vertices by type:**
- Alpha: 0,1,2,3,5,18 (weights: 20,20,15,20,15,40)
- Beta: 4,6,7,8,11,19 (weights: 30,30,30,18,12,40)
- Gamma: 12,13,14,17 (weights: 25,25,20,19)
- Delta: 9,10,15,16 (weights: 10,10,5,5)

**Key observations:**
1. The expected answer is size 6 with vertices {2,5,8,11,14,17}
2. Let me verify this clique:
   - Types: 2(alpha), 5(alpha), 8(beta), 11(beta), 14(gamma), 17(gamma) → alpha:2, beta:2, gamma:2 ✓
   - Weight: 15+15+18+12+20+19 = 99 ≤ 100 ✓
   - Edges needed: All pairs must be connected

**Verifying edges for {2,5,8,11,14,17}:**
- (2,5) ✓, (2,8) ✓, (2,11) ✓, (2,14) ✓, (2,17) ✓
- (5,8) ✓, (5,11) ✓, (5,14) ✓, (5,17) ✓
- (8,11) ✓, (8,14) ✓, (8,17) ✓
- (11,14) ✓, (11,17) ✓
- (14,17) ✓

All edges exist! This is a valid clique of size 6.

**Can we do better (size 7)?**
To get size 7, we'd need to add another vertex while maintaining:
- Type constraint (max 2 per type)
- Weight constraint (total ≤ 100, current is 99)
- All edges must exist

With only 1 weight unit remaining, we can't add any vertex (minimum weight is 5).

Even if we tried a different combination, the weight constraint makes size 7 extremely difficult with the given weights.

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

  Input tokens:  1,034
  Output tokens: 780
  Total tokens:  1,814

COMPLETE

## System 1 Final Answer

```json
Looking at this problem, I need to find the largest clique that satisfies type diversity (max 2 per type) and weight limit (≤100).

Let me analyze the graph structure:

**Vertices by type:**
- Alpha: 0,1,2,3,5,18 (weights: 20,20,15,20,15,40)
- Beta: 4,6,7,8,11,19 (weights: 30,30,30,18,12,40)
- Gamma: 12,13,14,17 (weights: 25,25,20,19)
- Delta: 9,10,15,16 (weights: 10,10,5,5)

**Key observations:**
1. The expected answer is size 6 with vertices {2,5,8,11,14,17}
2. Let me verify this clique:
   - Types: 2(alpha), 5(alpha), 8(beta), 11(beta), 14(gamma), 17(gamma) → alpha:2, beta:2, gamma:2 ✓
   - Weight: 15+15+18+12+20+19 = 99 ≤ 100 ✓
   - Edges needed: All pairs must be connected

**Verifying edges for {2,5,8,11,14,17}:**
- (2,5) ✓, (2,8) ✓, (2,11) ✓, (2,14) ✓, (2,17) ✓
- (5,8) ✓, (5,11) ✓, (5,14) ✓, (5,17) ✓
- (8,11) ✓, (8,14) ✓, (8,17) ✓
- (11,14) ✓, (11,17) ✓
- (14,17) ✓

All edges exist! This is a valid clique of size 6.

**Can we do better (size 7)?**
To get size 7, we'd need to add another vertex while maintaining:
- Type constraint (max 2 per type)
- Weight constraint (total ≤ 100, current is 99)
- All edges must exist

With only 1 weight unit remaining, we can't add any vertex (minimum weight is 5).

Even if we tried a different combination, the weight constraint makes size 7 extremely difficult with the given weights.

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
