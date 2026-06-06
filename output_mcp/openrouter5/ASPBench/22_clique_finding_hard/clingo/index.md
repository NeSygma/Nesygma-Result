# Benchmark Report (MCP): ASPBench - 22_clique_finding_hard

**Provider:** openrouter5
**Model:** deepseek/deepseek-v4-flash
**Solver:** clingo
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 21.70s


 MCP CLINGO AGENT - Symbolic Reasoning

### Query
# Problem Statement Given an undirected graph where each vertex has a specific **type** and

**weight**, find the largest possible clique that satisfies two additional constraints: **type
diversity** (no more than 2 vertices of any single type) and **weight limit** (total weight ≤ 100).
## Instance Data **Graph:** 20 vertices (0-19) with the following properties: | Vertex | Type |
Weight | |--------|------|--------| | 0 | alpha | 20 | | 1 | alpha | 20 | | 2 | alpha | 15 | | 3 |
alpha | 20 | | 4 | beta | 30 | | 5 | alpha | 15 | | 6 | beta | 30 | | 7 | beta | 30 | | 8 | beta |
18 | | 9 | delta | 10 | | 10 | delta | 10 | | 11 | beta | 12 | | 12 | gamma | 25 | | 13 | gamma | 25
| | 14 | gamma | 20 | | 15 | delta | 5 | | 16 | delta | 5 | | 17 | gamma | 19 | | 18 | alpha | 40 |
| 19 | beta | 40 | **Edges (undirected):** ``` (0,1), (0,3), (0,4), (0,6), (0,7), (0,9), (0,10),
(1,3), (1,4), (1,6), (1,7), (1,9), (2,5), (2,8), (2,11), (2,14), (2,17), (2,18), (3,4), (3,6),
(3,7), (3,9), (4,6), (4,7), (4,9), (5,8), (5,11), (5,14), (5,17), (5,19), (6,7), (6,9), (7,9),
(8,11), (8,14), (8,17), (11,14), (11,17), (12,13), (14,17), (15,16) ``` ## Constraints 1. **Clique
Property**: For any two vertices u, v in the solution clique, the edge (u, v) **must** exist in the
graph. 2. **Type Diversity Constraint**: For any given type, the number of vertices of that type in
the clique **must** be at most 2. 3. **Weight Limit Constraint**: The sum of weights of **all**
vertices in the clique **must** be at most 100. ## Objective Find the **maximum-sized clique** that
satisfies all constraints. **Expected optimal clique size: 6** ## Output Format The solution must be
a JSON object with the following structure: ```json { "clique": [2, 5, 8, 11, 14, 17],
"clique_size": 6, "clique_edges": [ [2, 5], [2, 8], [2, 11], [2, 14], [2, 17], [5, 8], [5, 11], [5,
14], [5, 17], [8, 11], [8, 14], [8, 17], [11, 14], [11, 17], [14, 17] ], "clique_total_weight": 99,
"clique_type_distribution": { "alpha": 2, "beta": 2, "gamma": 2 } } ``` ### Field Descriptions -
`clique`: List of vertex IDs in the clique (sorted) - `clique_size`: Number of vertices in the
clique - `clique_edges`: List of all edges within the clique (sorted pairs) - `clique_total_weight`:
Sum of weights of all vertices in the clique - `clique_type_distribution`: Count of vertices by type
in the clique

  - write_and_run_clingo: Write ASP code to a file for Clingo, validate syntax, and immediately run it to get answer sets.

## Iteration 1




### TOKEN USAGE - Iteration 1

  Input tokens:  6,890
  Output tokens: 932
  Total tokens:  7,822

### Tool Call: write_and_run_clingo

  Args: {
  "filename": "clique.lp",
  "code": "%% Problem: Maximum Clique with Type Diversity and Weight Limit\n%% Graph: 20 vertices (0-19)\n\n%% Domain definitions\nvertex(0..19).\n\n%% Vertex types\ntype(0, alpha). type(1, alpha). type(2, alpha). type(3, alpha). type(5, alpha). type(18, alpha).\ntype(4, beta). type(6, beta). type(7, beta). type(8, beta). type(11, beta). type(19, beta).\ntype(9, delta). type(10, delta). type(15, delta). type(16, delta).\ntype(12, gamma). type(13, gamma). type(14, gamma). type(17, gamma).\n\n%% Vertex weights\nweight(0, 20). weight(1, 20). weight(2, 15). weight(3, 20). weight(4, 30).\nweight(5, 15). weight(6, 30). weight(7, 30). weight(8, 18). weight(9, 10).\nweight(10, 10). weight(11, 12). weight(12, 25). weight(13, 25). weight(14, 20).\nweight(15, 5). weight(16, 5). weight(17, 19). weight(18, 40). weight(19, 40).\n\n%% Edges (undirected)\nedge(0,1). edge(0,3). edge(0,4). edge(0,6). edge(0,7). edge(0,9). edge(0,10).\nedge(1,3). edge(1,4). edge(1,6). edge(1,7). edge(1,9).\nedge(2,5). edge(2,8). edge(2,11). edge(2,14). edge(2,17). edge(2,18).\nedge(3,4). edge(3,6). edge(3,7). edge(3,9).\nedge(4,6). edge(4,7). edge(4,9).\nedge(5,8). edge(5,11). edge(5,14). edge(5,17). edge(5,19).\nedge(6,7). edge(6,9).\nedge(7,9).\nedge(8,11). edge(8,14). edge(8,17).\nedge(11,14). edge(11,17).\nedge(12,13).\nedge(14,17).\nedge(15,16).\n\n%% Make edges symmetric\nedge(Y, X) :- edge(X, Y), X != Y.\n\n%% No self-loops\n:- edge(X, X).\n\n%% Choice: select vertices for the clique\n{ in_clique(V) } :- vertex(V).\n\n%% Constraint 1: Clique property - every pair of selected vertices must be connected\n:- in_clique(U), in_clique(V), U < V, not edge(U, V).\n\n%% Constraint 2: Type diversity - at most 2 vertices of any single type\n:- type(T, _), #count { V : in_clique(V), type(V, T) } > 2.\n\n%% Constraint 3: Weight limit - total weight <= 100\n:- #sum { W, V : in_clique(V), weight(V, W) } > 100.\n\n%% Objective: maximize clique size\n#maximize { 1, V : in_clique(V) }.\n\n%% Output predicates\nclique_size(N) :- N = #count { V : in_clique(V) }.\nclique_total_weight(W) :- W = #sum { Wt, V : in_clique(V), weight(V, Wt) }.\nclique_type_count(T, C) :- type(T, _), C = #count { V : in_clique(V), type(V, T) }.\n\n%% Show results\n#show in_clique/1.\n#show clique_size/1.\n#show clique_total_weight/1.\n#show clique_type_count/2.\n"
}

#### Result

[{'type': 'text', 'text': '{"status":"optimum_found","command":"clingo clique.lp 10 --outf=2 --time-limit=60","models":[["clique_type_count(0,0)","clique_type_count(1,0)","clique_type_count(2,0)","clique_type_count(3,0)","clique_type_count(5,0)","clique_type_count(18,0)","clique_type_count(4,0)","clique_type_count(6,0)","clique_type_count(7,0)","clique_type_count(8,0)","clique_type_count(11,0)","clique_type_count(19,0)","clique_type_count(9,0)","clique_type_count(10,0)","clique_type_count(15,0)","clique_type_count(16,0)","clique_type_count(12,0)","clique_type_count(13,0)","clique_type_count(14,0)","clique_type_count(17,0)","clique_total_weight(0)","clique_size(0)"],["clique_type_count(0,0)","clique_type_count(1,0)","clique_type_count(2,0)","clique_type_count(3,0)","clique_type_count(5,0)","clique_type_count(18,0)","clique_type_count(4,0)","clique_type_count(6,0)","clique_type_count(7,0)","clique_type_count(8,0)","clique_type_count(11,0)","clique_type_count(19,0)","clique_type_count(9,0)","clique_type_count(10,0)","clique_type_count(15,0)","clique_type_count(16,0)","clique_type_count(12,0)","clique_type_count(13,0)","clique_type_count(14,0)","clique_type_count(17,0)","in_clique(0)","clique_total_weight(20)","clique_size(1)"],["clique_type_count(0,0)","clique_type_count(1,0)","clique_type_count(2,0)","clique_type_count(3,0)","clique_type_count(5,0)","clique_type_count(18,0)","clique_type_count(4,0)","clique_type_count(6,0)","clique_type_count(7,0)","clique_type_count(8,0)","clique_type_count(11,0)","clique_type_count(19,0)","clique_type_count(9,0)","clique_type_count(10,0)","clique_type_count(15,0)","clique_type_count(16,0)","clique_type_count(12,0)","clique_type_count(13,0)","clique_type_count(14,0)","clique_type_count(17,0)","in_clique(0)","in_clique(6)","clique_total_weight(50)","clique_size(2)"],["clique_type_count(0,0)","clique_type_count(1,0)","clique_type_count(2,0)","clique_type_count(3,0)","clique_type_count(5,0)","clique_type_count(18,0)","clique_type_count(4,0)","clique_type_count(6,0)","clique_type_count(7,0)","clique_type_count(8,0)","clique_type_count(11,0)","clique_type_count(19,0)","clique_type_count(9,0)","clique_type_count(10,0)","clique_type_count(15,0)","clique_type_count(16,0)","clique_type_count(12,0)","clique_type_count(13,0)","clique_type_count(14,0)","clique_type_count(17,0)","in_clique(0)","in_clique(4)","in_clique(6)","clique_total_weight(80)","clique_size(3)"],["clique_type_count(0,0)","clique_type_count(1,0)","clique_type_count(2,0)","clique_type_count(3,0)","clique_type_count(5,0)","clique_type_count(18,0)","clique_type_count(4,0)","clique_type_count(6,0)","clique_type_count(7,0)","clique_type_count(8,0)","clique_type_count(11,0)","clique_type_count(19,0)","clique_type_count(9,0)","clique_type_count(10,0)","clique_type_count(15,0)","clique_type_count(16,0)","clique_type_count(12,0)","clique_type_count(13,0)","clique_type_count(14,0)","clique_type_count(17,0)","in_clique(0)","in_clique(4)","in_clique(6)","in_clique(9)","clique_total_weight(90)","clique_size(4)"],["clique_type_count(0,0)","clique_type_count(1,0)","clique_type_count(2,0)","clique_type_count(3,0)","clique_type_count(5,0)","clique_type_count(18,0)","clique_type_count(4,0)","clique_type_count(6,0)","clique_type_count(7,0)","clique_type_count(8,0)","clique_type_count(11,0)","clique_type_count(19,0)","clique_type_count(9,0)","clique_type_count(10,0)","clique_type_count(15,0)","clique_type_count(16,0)","clique_type_count(12,0)","clique_type_count(13,0)","clique_type_count(14,0)","clique_type_count(17,0)","in_clique(0)","in_clique(1)","in_clique(3)","in_clique(4)","in_clique(9)","clique_total_weight(100)","clique_size(5)"],["clique_type_count(0,0)","clique_type_count(1,0)","clique_type_count(2,0)","clique_type_count(3,0)","clique_type_count(5,0)","clique_type_count(18,0)","clique_type_count(4,0)","clique_type_count(6,0)","clique_type_count(7,0)","clique_type_count(8,0)","clique_type_count(11,0)","clique_type_count(19,0)","clique_type_count(9,0)","clique_type_count(10,0)","clique_type_count(15,0)","clique_type_count(16,0)","clique_type_count(12,0)","clique_type_count(13,0)","clique_type_count(14,0)","clique_type_count(17,0)","in_clique(2)","in_clique(5)","in_clique(8)","in_clique(11)","in_clique(14)","in_clique(17)","clique_total_weight(99)","clique_size(6)"]]}', 'id': 'lc_8d969abf-a9ac-46bb-a914-2534387a18e2'}]


## Iteration 2


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

### TOKEN USAGE - Iteration 2

  Input tokens:  3,069
  Output tokens: 185
  Total tokens:  3,254

TOKEN USAGE SUMMARY
  Total input tokens:  9,959
  Total output tokens: 1,117
  Total tokens:        11,076

COMPLETE

## Final Answer

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
