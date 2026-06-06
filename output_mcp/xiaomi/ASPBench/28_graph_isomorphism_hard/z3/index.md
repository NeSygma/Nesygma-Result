# Benchmark Report (MCP): ASPBench - 28_graph_isomorphism_hard

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Solver:** z3
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 54.27s


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


Looking at this problem, I need to:

1. Model two graphs with vertices, colors, special properties, and weighted edges
2. Find a bijection between vertices that preserves colors, special status, and edge weights
3. Ensure no forbidden 3-cycle (triangle with special vertex and total weight 60) is created

Let me analyze the graphs carefully first, then write the Z3 code.

**Key observations:**
- G1 vertices: 1-8, G2 vertices: a-h (mapped to indices 0-7)
- Red: {1,2,5,6} ↔ {a,b,e,f}, Blue: {3,4,7,8} ↔ {c,d,g,h}
- Special: {1} ↔ {a}
- Need to check for forbidden triangles with special vertex and total weight 60

### TOKEN USAGE - Iteration 1

  Input tokens:  6,882
  Output tokens: 2,807
  Total tokens:  9,689

### Tool Call: write_and_run_z3

  Args: {
  "filename": "graph_isomorphism.py",
  "code": "from z3 import *\n\n# Map G2 vertices to indices for Z3\n# G1: 1,2,3,4,5,6,7,8 -> indices 0,1,2,3,4,5,6,7\n# G2: a,b,c,d,e,f,g,h -> indices 0,1,2,3,4,5,6,7\n\n# Vertex index mapping\ng1_vertices = [1, 2, 3, 4, 5, 6, 7, 8]\ng2_vertices = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']\ng2_to_idx = {v: i for i, v in enumerate(g2_vertices)}\n\n# Colors: 0 = Red, 1 = Blue\ng1_color = {1: 0, 2: 0, 3: 1, 4: 1, 5: 0, 6: 0, 7: 1, 8: 1}\ng2_color = {'a': 0, 'b': 0, 'c': 1, 'd': 1, 'e': 0, 'f': 0, 'g': 1, 'h': 1}\n\n# Special vertices\ng1_special = {1}\ng2_special = {'a'}\n\n# Edges with weights (undirected) - store as (min_idx, max_idx, weight)\n# G1 edges (using 0-indexed)\ng1_edges = {}\ng1_edge_list = [\n    (1,3,10), (1,4,20), (2,3,20), (2,4,10),\n    (5,7,10), (5,8,20), (6,7,20), (6,8,10),\n    (1,5,30), (2,6,30), (3,7,40), (4,8,40)\n]\nfor u, v, w in g1_edge_list:\n    ui, vi = u - 1, v - 1  # convert to 0-indexed\n    g1_edges[(min(ui, vi), max(ui, vi))] = w\n\n# G2 edges (using 0-indexed)\ng2_edges = {}\ng2_edge_list = [\n    ('a','c',10), ('a','d',20), ('b','c',20), ('b','d',10),\n    ('e','g',10), ('e','h',20), ('f','g',20), ('f','h',10),\n    ('a','e',30), ('b','f',30), ('c','g',40), ('d','h',40)\n]\nfor u, v, w in g2_edge_list:\n    ui, vi = g2_to_idx[u], g2_to_idx[v]\n    g2_edges[(min(ui, vi), max(ui, vi))] = w\n\n# Z3 solver\nsolver = Solver()\n\n# Mapping variables: f[i] = which G2 vertex (0-7) G1 vertex i maps to\nf = [Int(f'f_{i}') for i in range(8)]\n\n# Constraint 1: Bijection - each f[i] in [0,7] and all distinct\nfor i in range(8):\n    solver.add(f[i] >= 0, f[i] <= 7)\nsolver.add(Distinct(f))\n\n# Constraint 2: Color preservation\nfor i in range(8):\n    g1_v = g1_vertices[i]\n    c1 = g1_color[g1_v]\n    # f[i] must map to a G2 vertex with the same color\n    solver.add(Or([And(f[i] == j, g2_color[g2_vertices[j]] == c1) for j in range(8)]))\n\n# Constraint 3: Special vertex preservation\nfor i in range(8):\n    g1_v = g1_vertices[i]\n    is_special_g1 = g1_v in g1_special\n    if is_special_g1:\n        # Must map to a special vertex in G2\n        solver.add(Or([And(f[i] == j, g2_vertices[j] in g2_special) for j in range(8)]))\n    else:\n        # Must NOT map to a special vertex in G2\n        for j in range(8):\n            if g2_vertices[j] in g2_special:\n                solver.add(f[i] != j)\n\n# Constraint 4: Edge and weight preservation\n# For every pair (i,j) in G1: edge exists iff edge (f[i], f[j]) exists with same weight\nfor i in range(8):\n    for j in range(i+1, 8):\n        g1_key = (i, j)\n        g1_has_edge = g1_key in g1_edges\n        \n        # For each possible mapping pair (mi, mj), check if G2 has corresponding edge\n        for mi in range(8):\n            for mj in range(mi+1, 8):\n                g2_key = (mi, mj)\n                g2_has_edge = g2_key in g2_edges\n                \n                if g1_has_edge and g2_has_edge:\n                    # Both have edges - weights must match\n                    solver.add(Implies(\n                        And(f[i] == mi, f[j] == mj),\n                        g1_edges[g1_key] == g2_edges[g2_key]\n                    ))\n                elif g1_has_edge and not g2_has_edge:\n                    # G1 has edge but G2 doesn't - this mapping is invalid\n                    solver.add(Not(And(f[i] == mi, f[j] == mj)))\n                elif not g1_has_edge and g2_has_edge:\n                    # G1 doesn't have edge but G2 does - this mapping is invalid\n                    solver.add(Not(And(f[i] == mi, f[j] == mj)))\n                # If neither has edge, no constraint needed\n\n# Constraint 5: Forbidden subgraph - no 3-cycle with special vertex and total weight 60\n# First, identify all triangles in G2 that involve a special vertex (vertex 0 = 'a')\n# and have total weight 60\n# Then ensure our mapping doesn't create such a triangle\n\n# Find all triangles in G2 involving vertex 0 ('a')\nforbidden_triangles = []\nfor j in range(1, 8):\n    for k in range(j+1, 8):\n        e1 = (min(0,j), max(0,j))\n        e2 = (min(0,k), max(0,k))\n        e3 = (min(j,k), max(j,k))\n        if e1 in g2_edges and e2 in g2_edges and e3 in g2_edges:\n            total_w = g2_edges[e1] + g2_edges[e2] + g2_edges[e3]\n            if total_w == 60:\n                forbidden_triangles.append((0, j, k))\n\nprint(f\"Forbidden triangles in G2 (special vertex + weight 60): {forbidden_triangles}\")\nfor t in forbidden_triangles:\n    print(f\"  Triangle: {g2_vertices[t[0]]}, {g2_vertices[t[1]]}, {g2_vertices[t[2]]}\")\n    print(f\"  Weights: {g2_edges[(min(t[0],t[1]),max(t[0],t[1]))]}, {g2_edges[(min(t[0],t[2]),max(t[0],t[2]))]}, {g2_edges[(min(t[1],t[2]),max(t[1],t[2]))]}\")\n\n# For each forbidden triangle, ensure our mapping doesn't create it\n# A triangle (0, j, k) in G2 is \"created\" if there exist G1 vertices u, v, w\n# such that f(u)=0, f(v)=j, f(w)=k AND (u,v), (u,w), (v,w) are all edges in G1\nfor tri in forbidden_triangles:\n    a2, b2, c2 = tri  # G2 triangle vertices\n    # Find all triples in G1 that could map to this triangle\n    for u in range(8):\n        for v in range(u+1, 8):\n            for w in range(v+1, 8):\n                # Check if (u,v), (u,w), (v,w) are all edges in G1\n                e_uv = (min(u,v), max(u,v))\n                e_uw = (min(u,w), max(u,w))\n                e_vw = (min(v,w), max(v,w))\n                if e_uv in g1_edges and e_uw in g1_edges and e_vw in g1_edges:\n                    # This triple forms a triangle in G1\n                    # Forbid mapping to the forbidden G2 triangle\n                    # The mapping could be any permutation of (a2, b2, c2)\n                    from itertools import permutations\n                    for perm in permutations([a2, b2, c2]):\n                        solver.add(Not(And(\n                            f[u] == perm[0],\n                            f[v] == perm[1],\n                            f[w] == perm[2]\n                        )))\n\n# Check satisfiability\nBENCHMARK_MODE = True\nresult = solver.check()\n\nif result == sat:\n    model = solver.model()\n    print(\"STATUS: sat\")\n    print(\"Graphs are isomorphic!\")\n    \n    # Build mapping\n    mapping = {}\n    for i in range(8):\n        g1_v = str(g1_vertices[i])\n        g2_idx = model.evaluate(f[i]).as_long()\n        g2_v = g2_vertices[g2_idx]\n        mapping[g1_v] = g2_v\n    \n    print(f\"is_isomorphic: True\")\n    print(f\"mapping: {mapping}\")\n    \n    # Show preserved edges\n    preserved = []\n    for (i, j), w in g1_edges.items():\n        mi = model.evaluate(f[i]).as_long()\n        mj = model.evaluate(f[j]).as_long()\n        g2_key = (min(mi, mj), max(mi, mj))\n        if g2_key in g2_edges:\n            g1_edge = [str(g1_vertices[i]), str(g1_vertices[j])]\n            g2_edge = [g2_vertices[mi], g2_vertices[mj]]\n            preserved.append([sorted(g1_edge), sorted(g2_edge)])\n    \n    print(f\"preserved_weighted_edges: {preserved}\")\n    \n    # Verify no forbidden triangle is created\n    print(\"\\nVerification - checking for forbidden triangles in mapping:\")\n    for tri in forbidden_triangles:\n        a2, b2, c2 = tri\n        # Find which G1 vertices map to these\n        mapped = {}\n        for i in range(8):\n            idx = model.evaluate(f[i]).as_long()\n            if idx in [a2, b2, c2]:\n                mapped[g2_vertices[idx]] = g1_vertices[i]\n        if len(mapped) == 3:\n            print(f\"  G2 triangle ({g2_vertices[a2]},{g2_vertices[b2]},{g2_vertices[c2]}) maps to G1 vertices: {mapped}\")\n            # Check if these form a triangle in G1\n            verts = list(mapped.values())\n            all_edges = True\n            for x in range(3):\n                for y in range(x+1, 3):\n                    key = (min(verts[x]-1, verts[y]-1), max(verts[x]-1, verts[y]-1))\n                    if key not in g1_edges:\n                        all_edges = False\n            print(f\"    Forms triangle in G1: {all_edges}\")\n\nelif result == unsat:\n    print(\"STATUS: unsat\")\n    if BENCHMARK_MODE:\n        print(\"RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)\")\n    print(\"No valid isomorphism exists under the given constraints.\")\nelse:\n    print(\"STATUS: unknown\")\n"
}

#### Result

[{'type': 'text', 'text': '{"status":"success","stdout":"Forbidden triangles in G2 (special vertex + weight 60): []\\r\\nSTATUS: sat\\r\\nGraphs are isomorphic!\\r\\nis_isomorphic: True\\r\\nmapping: {\'1\': \'a\', \'2\': \'b\', \'3\': \'c\', \'4\': \'d\', \'5\': \'e\', \'6\': \'f\', \'7\': \'g\', \'8\': \'h\'}\\r\\npreserved_weighted_edges: [[[\'1\', \'3\'], [\'a\', \'c\']], [[\'1\', \'4\'], [\'a\', \'d\']], [[\'2\', \'3\'], [\'b\', \'c\']], [[\'2\', \'4\'], [\'b\', \'d\']], [[\'5\', \'7\'], [\'e\', \'g\']], [[\'5\', \'8\'], [\'e\', \'h\']], [[\'6\', \'7\'], [\'f\', \'g\']], [[\'6\', \'8\'], [\'f\', \'h\']], [[\'1\', \'5\'], [\'a\', \'e\']], [[\'2\', \'6\'], [\'b\', \'f\']], [[\'3\', \'7\'], [\'c\', \'g\']], [[\'4\', \'8\'], [\'d\', \'h\']]]\\r\\n\\r\\nVerification - checking for forbidden triangles in mapping:\\r\\n","stderr":null}', 'id': 'lc_e960cee2-e0ef-4bbc-9290-e89080f3ca8c'}]


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

  Input tokens:  1,893
  Output tokens: 341
  Total tokens:  2,234

TOKEN USAGE SUMMARY
  Total input tokens:  8,775
  Total output tokens: 3,148
  Total tokens:        11,923

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
