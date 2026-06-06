# Benchmark Report (MCP): ASPBench - 28_graph_isomorphism_easy

**Provider:** openrouter5
**Model:** deepseek/deepseek-v4-flash
**Solver:** z3
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 35.79s


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




### TOKEN USAGE - Iteration 1

  Input tokens:  6,821
  Output tokens: 1,088
  Total tokens:  7,909

### Tool Call: write_and_run_z3

  Args: {
  "filename": "graph_isomorphism.py",
  "code": "from z3 import *\n\n# Graph 1 vertices: 0, 1, 2, 3, 4\n# Graph 2 vertices: a, b, c, d, e (we'll map to indices 0..4)\n# G2 vertex names as strings for output\ng2_names = ['a', 'b', 'c', 'd', 'e']\n\n# Edges of G1 (as pairs of vertex indices)\ng1_edges = [(0,1), (0,2), (1,3), (2,4), (3,4)]\n\n# Edges of G2 (as pairs of vertex indices 0..4)\ng2_edges = [(0,1), (0,2), (1,3), (2,4), (3,4)]\n\n# Build adjacency sets for quick checking\ng1_adj = {i: set() for i in range(5)}\nfor u,v in g1_edges:\n    g1_adj[u].add(v)\n    g1_adj[v].add(u)\n\ng2_adj = {i: set() for i in range(5)}\nfor u,v in g2_edges:\n    g2_adj[u].add(v)\n    g2_adj[v].add(u)\n\n# Degree of each vertex\ng1_deg = [len(g1_adj[i]) for i in range(5)]\ng2_deg = [len(g2_adj[i]) for i in range(5)]\n\nsolver = Solver()\n\n# f[i] = the G2 vertex (0..4) that G1 vertex i maps to\nf = [Int(f'f_{i}') for i in range(5)]\n\n# Domain: each f[i] is a G2 vertex index\nfor i in range(5):\n    solver.add(f[i] >= 0, f[i] <= 4)\n\n# Bijection: all f[i] are distinct (injective + same cardinality = bijective)\nsolver.add(Distinct(f))\n\n# Degree preservation: degree of G1 vertex i must equal degree of G2 vertex f[i]\nfor i in range(5):\n    # Use Or-loop to constrain degree\n    solver.add(Or([And(f[i] == j, g1_deg[i] == g2_deg[j]) for j in range(5)]))\n\n# Adjacency preservation: for every edge (u,v) in G1, (f(u), f(v)) must be an edge in G2\nfor u, v in g1_edges:\n    # (f[u], f[v]) must be an edge in G2\n    # Build a constraint that checks all possible pairs\n    edge_constraints = []\n    for j in range(5):\n        for k in range(5):\n            if (j, k) in g2_edges or (k, j) in g2_edges:\n                edge_constraints.append(And(f[u] == j, f[v] == k))\n    solver.add(Or(edge_constraints))\n\n# Reverse preservation: for every edge (j,k) in G2, there must be an edge (u,v) in G1\n# such that f(u)=j and f(v)=k (or f(u)=k and f(v)=j)\nfor j, k in g2_edges:\n    reverse_constraints = []\n    for u, v in g1_edges:\n        # Either (f[u]=j and f[v]=k) or (f[u]=k and f[v]=j)\n        reverse_constraints.append(Or(And(f[u] == j, f[v] == k), And(f[u] == k, f[v] == j)))\n    solver.add(Or(reverse_constraints))\n\nBENCHMARK_MODE = True\nresult = solver.check()\n\nif result == sat:\n    m = solver.model()\n    print(\"STATUS: sat\")\n    print(\"is_isomorphic: true\")\n    \n    # Build mapping\n    mapping = {}\n    for i in range(5):\n        g2_idx = m.eval(f[i]).as_long()\n        mapping[str(i)] = g2_names[g2_idx]\n    print(f\"mapping: {mapping}\")\n    \n    # Build preserved edges\n    preserved = []\n    for u, v in g1_edges:\n        fu = g2_names[m.eval(f[u]).as_long()]\n        fv = g2_names[m.eval(f[v]).as_long()]\n        preserved.append([f\"{u},{v}\", f\"{fu},{fv}\"])\n    print(f\"preserved_edges: {preserved}\")\n    \nelif result == unsat:\n    print(\"STATUS: unsat\")\n    if BENCHMARK_MODE:\n        print(\"RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)\")\nelse:\n    print(\"STATUS: unknown\")\n"
}

#### Result

[{'type': 'text', 'text': '{"status":"success","stdout":"STATUS: sat\\r\\nis_isomorphic: true\\r\\nmapping: {\'0\': \'a\', \'1\': \'b\', \'2\': \'c\', \'3\': \'d\', \'4\': \'e\'}\\r\\npreserved_edges: [[\'0,1\', \'a,b\'], [\'0,2\', \'a,c\'], [\'1,3\', \'b,d\'], [\'2,4\', \'c,e\'], [\'3,4\', \'d,e\']]\\r\\n","stderr":null}', 'id': 'lc_657d62a0-b591-453f-b668-d8f272f50c28'}]


## Iteration 2


```json
{
  "is_isomorphic": true,
  "mapping": {"0": "a", "1": "b", "2": "c", "3": "d", "4": "e"},
  "preserved_edges": [["0,1", "a,b"], ["0,2", "a,c"], ["1,3", "b,d"], ["2,4", "c,e"], ["3,4", "d,e"]]
}
```

### TOKEN USAGE - Iteration 2

  Input tokens:  1,103
  Output tokens: 103
  Total tokens:  1,206

TOKEN USAGE SUMMARY
  Total input tokens:  7,924
  Total output tokens: 1,191
  Total tokens:        9,115

COMPLETE

## Final Answer

```json
```json
{
  "is_isomorphic": true,
  "mapping": {"0": "a", "1": "b", "2": "c", "3": "d", "4": "e"},
  "preserved_edges": [["0,1", "a,b"], ["0,2", "a,c"], ["1,3", "b,d"], ["2,4", "c,e"], ["3,4", "d,e"]]
}
```
```
