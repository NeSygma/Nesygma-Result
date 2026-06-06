# Benchmark Report (MCP): ASPBench - 28_graph_isomorphism_easy

**Provider:** openrouter3
**Model:** xiaomi/mimo-v2-flash
**Solver:** z3
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 22.62s


 MCP Z3 AGENT - Symbolic Reasoning

### Query
# Problem Statement Determine if two given graphs are isomorphic by finding a bijection between

their vertices that preserves adjacency relationships. ## Instance Data **Graph 1 (G1)** Vertices:
0, 1, 2, 3, 4 Edges: - (0, 1) - (0, 2) - (1, 3) - (2, 4) - (3, 4) **Graph 2 (G2)** Vertices: a, b,
c, d, e Edges: - (a, b) - (a, c) - (b, d) - (c, e) - (d, e) ## Constraints 1. **Bijection**: There
must exist a bijection f: V1 → V2 mapping G1 vertices to G2 vertices 2. **Adjacency preservation**:
For **all** edges (u,v) in G1, the mapped edge (f(u),f(v)) **must** exist in G2 3. **Reverse
preservation**: For **all** edges in G2, there **must** be a corresponding edge in G1 4. **Degree
preservation**: Vertex degrees **must** be preserved under the mapping ## Objective Determine if the
graphs are isomorphic and find the vertex mapping if one exists. ## Output Format ```json {
"is_isomorphic": true, "mapping": {"0": "a", "1": "b", ...}, "preserved_edges": [["0,1", "a,b"],
["0,2", "a,c"], ...] } ``` **Field descriptions:** - `is_isomorphic` (boolean): Whether the graphs
are isomorphic - `mapping` (object or null): Vertex mapping from G1 to G2 as strings (null if not
isomorphic) - `preserved_edges` (array): Edge correspondence pairs as [["u,v", "f(u),f(v)"], ...]
(empty if not isomorphic)

  - write_and_run_z3: Write Python code using Z3 to a file and run it immediately to get results.
We capture printed stdout and stderr from running the script.

## Iteration 1


I'll solve this graph isomorphism problem using Z3. Let me analyze the problem and create a Z3 script to find the bijection between the two graphs.

## Phase 1: Analysis & Modeling

**Entities:**
- Graph 1 vertices: 0, 1, 2, 3, 4
- Graph 2 vertices: a, b, c, d, e
- Edges in G1: (0,1), (0,2), (1,3), (2,4), (3,4)
- Edges in G2: (a,b), (a,c), (b,d), (c,e), (d,e)

**Variables:**
- We need a bijection f: {0,1,2,3,4} → {a,b,c,d,e}
- Represent f as a mapping from each G1 vertex to a G2 vertex

**Constraints:**
1. Bijection: Each G1 vertex maps to exactly one G2 vertex, and all G2 vertices are used exactly once
2. Adjacency preservation: If (u,v) is an edge in G1, then (f(u),f(v)) must be an edge in G2
3. Reverse preservation: If (x,y) is an edge in G2, then there must be some (u,v) in G1 such that f(u)=x and f(v)=y
4. Degree preservation: The degree of each vertex in G1 must equal the degree of its image in G2

## Phase 2: Design and Write

I'll create a Z3 script that:
1. Declares symbolic variables for the mapping
2. Adds constraints for bijection, adjacency preservation, and degree preservation
3. Checks for satisfiability
4. If satisfiable, extracts the mapping and edge correspondences

### TOKEN USAGE - Iteration 1

  Input tokens:  6,565
  Output tokens: 1,924
  Total tokens:  8,489

### Tool Call: write_and_run_z3

  Args: {
  "filename": "graph_isomorphism.py",
  "code": "from z3 import *\n\n# Graph data\ng1_vertices = [0, 1, 2, 3, 4]\ng2_vertices = ['a', 'b', 'c', 'd', 'e']\n\ng1_edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4)]\ng2_edges = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'e'), ('d', 'e')]\n\n# Create mapping from G1 vertex indices to G2 vertex strings\n# We'll use an array where f[i] represents the mapping of G1 vertex i\nf = [Int(f'f_{i}') for i in range(len(g1_vertices))]\n\nsolver = Solver()\n\n# Constraint 1: Bijection - each G1 vertex maps to a unique G2 vertex\n# f[i] should be in range 0..4 (representing indices of g2_vertices)\nfor i in range(len(g1_vertices)):\n    solver.add(f[i] >= 0)\n    solver.add(f[i] < len(g2_vertices))\n\n# All f[i] must be distinct (bijection)\nsolver.add(Distinct(f))\n\n# Constraint 2: Adjacency preservation\n# For each edge (u,v) in G1, (f(u), f(v)) must be an edge in G2\n# We need to check if the mapped vertices form an edge in G2\nfor (u, v) in g1_edges:\n    # Check if (f[u], f[v]) is an edge in G2\n    edge_exists = False\n    for (g2_u, g2_v) in g2_edges:\n        # Map G2 vertex strings to indices\n        g2_u_idx = g2_vertices.index(g2_u)\n        g2_v_idx = g2_vertices.index(g2_v)\n        # Add constraint: if f[u] == g2_u_idx and f[v] == g2_v_idx, then this edge is preserved\n        # We need to ensure that for each G1 edge, there exists some G2 edge that matches\n        # Actually, we need to ensure that the specific mapping produces an edge in G2\n        # So we need: (f[u] == g2_u_idx AND f[v] == g2_v_idx) OR (f[u] == g2_v_idx AND f[v] == g2_u_idx)\n        # But we need this to be true for at least one G2 edge\n        # Better approach: For each G1 edge, the pair (f[u], f[v]) must equal some G2 edge pair\n        pass\n\n# Let's use a different approach: For each G1 edge, create a constraint that\n# the mapped vertices form an edge in G2\nfor (u, v) in g1_edges:\n    # Create disjunction over all G2 edges\n    edge_preserved = []\n    for (g2_u, g2_v) in g2_edges:\n        g2_u_idx = g2_vertices.index(g2_u)\n        g2_v_idx = g2_vertices.index(g2_v)\n        # The edge can be in either direction\n        edge_preserved.append(And(f[u] == g2_u_idx, f[v] == g2_v_idx))\n        edge_preserved.append(And(f[u] == g2_v_idx, f[v] == g2_u_idx))\n    solver.add(Or(edge_preserved))\n\n# Constraint 3: Reverse preservation - every G2 edge must correspond to some G1 edge\n# For each G2 edge, there must exist some G1 edge (u,v) such that f[u] and f[v] map to the G2 vertices\nfor (g2_u, g2_v) in g2_edges:\n    g2_u_idx = g2_vertices.index(g2_u)\n    g2_v_idx = g2_vertices.index(g2_v)\n    # Create disjunction over all G1 edges\n    corresponding_g1_edge = []\n    for (u, v) in g1_edges:\n        # The G1 edge can map to the G2 edge in either direction\n        corresponding_g1_edge.append(And(f[u] == g2_u_idx, f[v] == g2_v_idx))\n        corresponding_g1_edge.append(And(f[u] == g2_v_idx, f[v] == g2_u_idx))\n    solver.add(Or(corresponding_g1_edge))\n\n# Constraint 4: Degree preservation\n# Calculate degrees for G1\ng1_degrees = {}\nfor v in g1_vertices:\n    g1_degrees[v] = 0\nfor (u, v) in g1_edges:\n    g1_degrees[u] += 1\n    g1_degrees[v] += 1\n\n# Calculate degrees for G2\ng2_degrees = {}\nfor v in g2_vertices:\n    g2_degrees[v] = 0\nfor (u, v) in g2_edges:\n    g2_degrees[u] += 1\n    g2_degrees[v] += 1\n\n# For each G1 vertex, its degree must equal the degree of its image in G2\nfor v in g1_vertices:\n    # Create constraint: degree of v equals degree of f[v]\n    # We need to express this using the mapping f[v]\n    degree_constraint = []\n    for g2_v_idx, g2_v in enumerate(g2_vertices):\n        # If f[v] maps to g2_v_idx, then g1_degrees[v] must equal g2_degrees[g2_v]\n        degree_constraint.append(Implies(f[v] == g2_v_idx, g1_degrees[v] == g2_degrees[g2_v]))\n    solver.add(Or(degree_constraint))\n\n# Check satisfiability\nresult = solver.check()\n\nif result == sat:\n    model = solver.model()\n    print(\"STATUS: sat\")\n    \n    # Extract mapping\n    mapping = {}\n    for i, v in enumerate(g1_vertices):\n        g2_idx = model[f[i]].as_long()\n        mapping[str(v)] = g2_vertices[g2_idx]\n    \n    print(\"is_isomorphic: True\")\n    print(\"mapping:\", mapping)\n    \n    # Extract preserved edges\n    preserved_edges = []\n    for (u, v) in g1_edges:\n        g2_u_idx = model[f[u]].as_long()\n        g2_v_idx = model[f[v]].as_long()\n        g2_u = g2_vertices[g2_u_idx]\n        g2_v = g2_vertices[g2_v_idx]\n        preserved_edges.append([f\"{u},{v}\", f\"{g2_u},{g2_v}\"])\n    \n    print(\"preserved_edges:\", preserved_edges)\n    \nelif result == unsat:\n    print(\"STATUS: unsat\")\n    print(\"is_isomorphic: False\")\n    print(\"mapping: null\")\n    print(\"preserved_edges: []\")\nelse:\n    print(\"STATUS: unknown\")\n    print(\"is_isomorphic: unknown\")\n    print(\"mapping: null\")\n    print(\"preserved_edges: []\")"
}

#### Result

[{'type': 'text', 'text': '{"status":"success","stdout":"STATUS: sat\\r\\nis_isomorphic: True\\r\\nmapping: {\'0\': \'a\', \'1\': \'b\', \'2\': \'c\', \'3\': \'d\', \'4\': \'e\'}\\r\\npreserved_edges: [[\'0,1\', \'a,b\'], [\'0,2\', \'a,c\'], [\'1,3\', \'b,d\'], [\'2,4\', \'c,e\'], [\'3,4\', \'d,e\']]\\r\\n","stderr":null}', 'id': 'lc_b212b978-0975-43a2-afa5-94cc5e4db29a'}]


## Iteration 2


{
  "is_isomorphic": true,
  "mapping": {"0": "a", "1": "b", "2": "c", "3": "d", "4": "e"},
  "preserved_edges": [["0,1", "a,b"], ["0,2", "a,c"], ["1,3", "b,d"], ["2,4", "c,e"], ["3,4", "d,e"]]
}

### TOKEN USAGE - Iteration 2

  Input tokens:  1,084
  Output tokens: 96
  Total tokens:  1,180

TOKEN USAGE SUMMARY
  Total input tokens:  7,649
  Total output tokens: 2,020
  Total tokens:        9,669

COMPLETE

## Final Answer

```json
{
  "is_isomorphic": true,
  "mapping": {"0": "a", "1": "b", "2": "c", "3": "d", "4": "e"},
  "preserved_edges": [["0,1", "a,b"], ["0,2", "a,c"], ["1,3", "b,d"], ["2,4", "c,e"], ["3,4", "d,e"]]
}
```
