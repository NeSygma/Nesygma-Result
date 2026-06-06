# Benchmark Report (MCP): ASPBench - 28_graph_isomorphism_hard

**Provider:** openrouter5
**Model:** deepseek/deepseek-v4-flash
**Solver:** z3
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 44.24s


 MCP Z3 AGENT - Symbolic Reasoning

### Query
# Problem Statement Determine if two weighted, colored graphs are isomorphic while avoiding

forbidden subgraph patterns. An isomorphism must preserve vertex colors, edge weights, special
vertex properties, and must not create any 3-cycle involving a special vertex with total edge weight
of exactly 60. ## Instance Data **Graph G1:** - Vertices: 1, 2, 3, 4, 5, 6, 7, 8 - Colors: - Red
vertices: 1, 2, 5, 6 - Blue vertices: 3, 4, 7, 8 - Special vertices: 1 - Edges (undirected, with
weights): - (1,3,10), (1,4,20), (2,3,20), (2,4,10) - (5,7,10), (5,8,20), (6,7,20), (6,8,10) -
(1,5,30), (2,6,30), (3,7,40), (4,8,40) **Graph G2:** - Vertices: a, b, c, d, e, f, g, h - Colors: -
Red vertices: a, b, e, f - Blue vertices: c, d, g, h - Special vertices: a - Edges (undirected, with
weights): - (a,c,10), (a,d,20), (b,c,20), (b,d,10) - (e,g,10), (e,h,20), (f,g,20), (f,h,10) -
(a,e,30), (b,f,30), (c,g,40), (d,h,40) ## Constraints 1. **Bijection**: The mapping f: V1 → V2 must
be one-to-one and onto 2. **Color Preservation**: Color of vertex v in G1 must equal color of f(v)
in G2 3. **Special Vertex Preservation**: Vertex v is special in G1 if and only if f(v) is special
in G2 4. **Edge and Weight Preservation**: Edge (u,v) with weight w exists in G1 if and only if edge
(f(u),f(v)) with weight w exists in G2 5. **Forbidden Subgraph**: The mapping is invalid if it
creates a 3-cycle (triangle) in G2 that involves a special vertex and has total edge weight exactly
60 ## Objective Find a valid isomorphism mapping between G1 and G2, or determine that no such
mapping exists. ## Output Format The solution must be a JSON object: ```json { "is_isomorphic":
true, "mapping": { "1": "a", "2": "b", "3": "c", "4": "d", "5": "e", "6": "f", "7": "g", "8": "h" },
"preserved_weighted_edges": [ [["1", "3", 10], ["a", "c", 10]], [["1", "4", 20], ["a", "d", 20]],
[["1", "5", 30], ["a", "e", 30]], [["2", "3", 20], ["b", "c", 20]], [["2", "4", 10], ["b", "d",
10]], [["2", "6", 30], ["b", "f", 30]], [["3", "7", 40], ["c", "g", 40]], [["4", "8", 40], ["d",
"h", 40]], [["5", "7", 10], ["e", "g", 10]], [["5", "8", 20], ["e", "h", 20]], [["6", "7", 20],
["f", "g", 20]], [["6", "8", 10], ["f", "h", 10]] ] } ``` **Field Descriptions:** - `is_isomorphic`:
Boolean indicating if graphs are isomorphic - `mapping`: Object mapping G1 vertex (as string) to G2
vertex (as string), or null if not isomorphic - `preserved_weighted_edges`: Array of edge mappings
showing [[G1_edge], [G2_edge]] pairs, where edges are normalized (sorted vertices)

  - write_and_run_z3: Write Python code using Z3 to a file and run it immediately to get results.
We capture printed stdout and stderr from running the script.

## Iteration 1




### TOKEN USAGE - Iteration 1

  Input tokens:  7,109
  Output tokens: 2,588
  Total tokens:  9,697

### Tool Call: write_and_run_z3

  Args: {
  "filename": "graph_isomorphism.py",
  "code": "from z3 import *\n\n# Create solver\nsolver = Solver()\n\n# G1 vertices: 1,2,3,4,5,6,7,8\n# G2 vertices: a,b,c,d,e,f,g,h (we'll encode as 0..7)\ng1_vertices = [1, 2, 3, 4, 5, 6, 7, 8]\ng2_vertices = [0, 1, 2, 3, 4, 5, 6, 7]  # a=0, b=1, c=2, d=3, e=4, f=5, g=6, h=7\n\n# Map G2 vertex names to indices\ng2_names = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'}\n\n# Colors: Red=0, Blue=1\n# G1 colors: Red: 1,2,5,6; Blue: 3,4,7,8\ng1_colors = {1: 0, 2: 0, 3: 1, 4: 1, 5: 0, 6: 0, 7: 1, 8: 1}\n# G2 colors: Red: a,b,e,f (0,1,4,5); Blue: c,d,g,h (2,3,6,7)\ng2_colors = {0: 0, 1: 0, 2: 1, 3: 1, 4: 0, 5: 0, 6: 1, 7: 1}\n\n# Special vertices: G1: {1}, G2: {a=0}\ng1_special = {1}\ng2_special = {0}\n\n# Edges for G1: (u,v,w) - undirected\ng1_edges = [\n    (1,3,10), (1,4,20), (2,3,20), (2,4,10),\n    (5,7,10), (5,8,20), (6,7,20), (6,8,10),\n    (1,5,30), (2,6,30), (3,7,40), (4,8,40)\n]\n\n# Edges for G2: (u,v,w) - undirected, using indices\ng2_edges = [\n    (0,2,10), (0,3,20), (1,2,20), (1,3,10),\n    (4,6,10), (4,7,20), (5,6,20), (5,7,10),\n    (0,4,30), (1,5,30), (2,6,40), (3,7,40)\n]\n\n# Build adjacency sets for quick lookup\ng1_adj = {}\nfor u,v,w in g1_edges:\n    g1_adj.setdefault((u,v), w)\n    g1_adj.setdefault((v,u), w)\n\ng2_adj = {}\nfor u,v,w in g2_edges:\n    g2_adj.setdefault((u,v), w)\n    g2_adj.setdefault((v,u), w)\n\n# Decision variables: f[i] = G2 vertex index that G1 vertex i maps to\nf = [Int(f'f_{i}') for i in range(1, 9)]  # index by G1 vertex number\n\n# Domain: each f[i] is in {0..7}\nfor i in range(1, 9):\n    solver.add(f[i-1] >= 0, f[i-1] <= 7)\n\n# Constraint 1: Bijection - one-to-one and onto\nsolver.add(Distinct(f))\n\n# Constraint 2: Color preservation\nfor v in range(1, 9):\n    # f(v) must have same color as v\n    # Use Or-loop to constrain\n    same_color_conds = []\n    for g2v in range(8):\n        if g1_colors[v] == g2_colors[g2v]:\n            same_color_conds.append(f[v-1] == g2v)\n    solver.add(Or(same_color_conds))\n\n# Constraint 3: Special vertex preservation\n# Vertex 1 is special in G1, must map to special vertex in G2 (which is a=0)\nsolver.add(f[0] == 0)  # 1 -> a\n\n# Constraint 4: Edge and weight preservation\n# For every pair of G1 vertices (u,v), check if edge exists in G1\n# If edge (u,v,w) in G1, then (f(u), f(v), w) must be in G2\n# If no edge in G1, then (f(u), f(v)) must not be an edge in G2\n\nfor u in range(1, 9):\n    for v in range(u+1, 9):\n        edge_key = (u,v) if (u,v) in g1_adj else (v,u)\n        if edge_key in g1_adj:\n            w = g1_adj[edge_key]\n            # Edge exists in G1 with weight w\n            # So (f(u), f(v), w) must exist in G2\n            edge_conds = []\n            for (g2u, g2v, g2w) in g2_edges:\n                edge_conds.append(And(f[u-1] == g2u, f[v-1] == g2v, w == g2w))\n                edge_conds.append(And(f[u-1] == g2v, f[v-1] == g2u, w == g2w))\n            solver.add(Or(edge_conds))\n        else:\n            # No edge in G1\n            # So (f(u), f(v)) must not be an edge in G2\n            no_edge_conds = []\n            for (g2u, g2v, _) in g2_edges:\n                no_edge_conds.append(Not(And(f[u-1] == g2u, f[v-1] == g2v)))\n                no_edge_conds.append(Not(And(f[u-1] == g2v, f[v-1] == g2u)))\n            solver.add(And(no_edge_conds))\n\n# Constraint 5: Forbidden subgraph - no 3-cycle involving special vertex (a=0) with total weight exactly 60\n# Special vertex in G2 is a=0, which is f[0] (mapping of G1 vertex 1)\n# We need to check all triples (0, x, y) where x,y are distinct G2 vertices\n# If (0,x), (0,y), (x,y) are all edges, and weights sum to 60, it's forbidden\n\n# Build G2 edge weight lookup\ng2_edge_weights = {}\nfor u,v,w in g2_edges:\n    g2_edge_weights[(u,v)] = w\n    g2_edge_weights[(v,u)] = w\n\n# For each pair of G2 vertices (x,y) distinct from 0\nfor x in range(1, 8):\n    for y in range(x+1, 8):\n        # Check if triangle (0,x,y) exists in G2\n        if (0,x) in g2_edge_weights and (0,y) in g2_edge_weights and (x,y) in g2_edge_weights:\n            total_w = g2_edge_weights[(0,x)] + g2_edge_weights[(0,y)] + g2_edge_weights[(x,y)]\n            if total_w == 60:\n                # This triangle is forbidden. The mapping must not map any G1 vertices to x and y\n                # such that the corresponding G1 vertices also form a triangle with vertex 1\n                # Actually, the constraint says: the mapping is invalid if it CREATES a 3-cycle in G2\n                # that involves a special vertex and has total weight exactly 60.\n                # Since the special vertex is fixed at a=0, and the edges/weights are preserved,\n                # this means we must avoid mapping G1 vertices to x,y such that the pre-images\n                # in G1 form a triangle with vertex 1 with total weight 60.\n                \n                # Find which G1 vertices could map to x and y\n                # The forbidden condition is: there exist G1 vertices u,v such that\n                # f(u)=x, f(v)=y, and (1,u,w1), (1,v,w2), (u,v,w3) are edges in G1 with w1+w2+w3=60\n                \n                # Check all pairs of G1 vertices (u,v) distinct from 1\n                for u in range(2, 9):\n                    for v in range(u+1, 9):\n                        # Check if (1,u), (1,v), (u,v) are edges in G1\n                        e1u = (1,u) if (1,u) in g1_adj else (u,1) if (u,1) in g1_adj else None\n                        e1v = (1,v) if (1,v) in g1_adj else (v,1) if (v,1) in g1_adj else None\n                        euv = (u,v) if (u,v) in g1_adj else (v,u) if (v,u) in g1_adj else None\n                        \n                        if e1u and e1v and euv:\n                            w1 = g1_adj[e1u]\n                            w2 = g1_adj[e1v]\n                            w3 = g1_adj[euv]\n                            if w1 + w2 + w3 == 60:\n                                # This would create a forbidden triangle\n                                solver.add(Not(And(f[u-1] == x, f[v-1] == y)))\n                                solver.add(Not(And(f[u-1] == y, f[v-1] == x)))\n\n# Check\nBENCHMARK_MODE = True\nresult = solver.check()\n\nif result == sat:\n    m = solver.model()\n    print(\"STATUS: sat\")\n    print(\"is_isomorphic: true\")\n    \n    # Build mapping\n    mapping = {}\n    for i in range(1, 9):\n        g2_idx = m.eval(f[i-1]).as_long()\n        mapping[str(i)] = g2_names[g2_idx]\n    \n    print(\"mapping:\", mapping)\n    \n    # Build preserved weighted edges\n    preserved_edges = []\n    for (u,v,w) in g1_edges:\n        g2_u = m.eval(f[u-1]).as_long()\n        g2_v = m.eval(f[v-1]).as_long()\n        g1_edge = sorted([str(u), str(v)])\n        g2_edge = sorted([g2_names[g2_u], g2_names[g2_v]])\n        preserved_edges.append([[g1_edge[0], g1_edge[1], w], [g2_edge[0], g2_edge[1], w]])\n    \n    print(\"preserved_weighted_edges:\", preserved_edges)\n    \nelif result == unsat:\n    print(\"STATUS: unsat\")\n    if BENCHMARK_MODE:\n        print(\"RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)\")\nelse:\n    print(\"STATUS: unknown\")\n"
}

#### Result

[{'type': 'text', 'text': '{"status":"success","stdout":"STATUS: sat\\r\\nis_isomorphic: true\\r\\nmapping: {\'1\': \'a\', \'2\': \'b\', \'3\': \'c\', \'4\': \'d\', \'5\': \'e\', \'6\': \'f\', \'7\': \'g\', \'8\': \'h\'}\\r\\npreserved_weighted_edges: [[[\'1\', \'3\', 10], [\'a\', \'c\', 10]], [[\'1\', \'4\', 20], [\'a\', \'d\', 20]], [[\'2\', \'3\', 20], [\'b\', \'c\', 20]], [[\'2\', \'4\', 10], [\'b\', \'d\', 10]], [[\'5\', \'7\', 10], [\'e\', \'g\', 10]], [[\'5\', \'8\', 20], [\'e\', \'h\', 20]], [[\'6\', \'7\', 20], [\'f\', \'g\', 20]], [[\'6\', \'8\', 10], [\'f\', \'h\', 10]], [[\'1\', \'5\', 30], [\'a\', \'e\', 30]], [[\'2\', \'6\', 30], [\'b\', \'f\', 30]], [[\'3\', \'7\', 40], [\'c\', \'g\', 40]], [[\'4\', \'8\', 40], [\'d\', \'h\', 40]]]\\r\\n","stderr":null}', 'id': 'lc_5d47a807-0630-4b25-9691-d28f959d00e9'}]


## Iteration 2


```json
{
  "is_isomorphic": true,
  "mapping": {
    "1": "a",
    "2": "b",
    "3": "c",
    "4": "d",
    "5": "e",
    "6": "f",
    "7": "g",
    "8": "h"
  },
  "preserved_weighted_edges": [
    [["1", "3", 10], ["a", "c", 10]],
    [["1", "4", 20], ["a", "d", 20]],
    [["2", "3", 20], ["b", "c", 20]],
    [["2", "4", 10], ["b", "d", 10]],
    [["5", "7", 10], ["e", "g", 10]],
    [["5", "8", 20], ["e", "h", 20]],
    [["6", "7", 20], ["f", "g", 20]],
    [["6", "8", 10], ["f", "h", 10]],
    [["1", "5", 30], ["a", "e", 30]],
    [["2", "6", 30], ["b", "f", 30]],
    [["3", "7", 40], ["c", "g", 40]],
    [["4", "8", 40], ["d", "h", 40]]
  ]
}
```

### TOKEN USAGE - Iteration 2

  Input tokens:  1,951
  Output tokens: 330
  Total tokens:  2,281

TOKEN USAGE SUMMARY
  Total input tokens:  9,060
  Total output tokens: 2,918
  Total tokens:        11,978

COMPLETE

## Final Answer

```json
```json
{
  "is_isomorphic": true,
  "mapping": {
    "1": "a",
    "2": "b",
    "3": "c",
    "4": "d",
    "5": "e",
    "6": "f",
    "7": "g",
    "8": "h"
  },
  "preserved_weighted_edges": [
    [["1", "3", 10], ["a", "c", 10]],
    [["1", "4", 20], ["a", "d", 20]],
    [["2", "3", 20], ["b", "c", 20]],
    [["2", "4", 10], ["b", "d", 10]],
    [["5", "7", 10], ["e", "g", 10]],
    [["5", "8", 20], ["e", "h", 20]],
    [["6", "7", 20], ["f", "g", 20]],
    [["6", "8", 10], ["f", "h", 10]],
    [["1", "5", 30], ["a", "e", 30]],
    [["2", "6", 30], ["b", "f", 30]],
    [["3", "7", 40], ["c", "g", 40]],
    [["4", "8", 40], ["d", "h", 40]]
  ]
}
```
```
