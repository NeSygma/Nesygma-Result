# Benchmark Report (MCP): ASPBench - 28_graph_isomorphism_easy

**Provider:** xiaomi
**Model:** mimo-v2.5-pro
**Solver:** z3
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: False, reasoning_effort: none
**Duration:** 22.87s


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

  Input tokens:  6,565
  Output tokens: 868
  Total tokens:  7,433

### Tool Call: write_and_run_z3

  Args: {
  "filename": "graph_isomorphism.py",
  "code": "\nfrom z3 import *\n\n# Graph definitions\n# G1 vertices: 0,1,2,3,4\n# G2 vertices: a,b,c,d,e (mapped to 0,1,2,3,4 internally)\n\n# G1 edges (undirected)\ng1_edges = [(0,1), (0,2), (1,3), (2,4), (3,4)]\n\n# G2 edges (undirected) - map a=0, b=1, c=2, d=3, e=4\ng2_edges = [(0,1), (0,2), (1,3), (2,4), (3,4)]\n\n# G2 vertex names for output\ng2_names = {0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e'}\n\nn = 5  # number of vertices\n\nsolver = Solver()\n\n# f[i] = the G2 vertex (0-4) that G1 vertex i maps to\nf = [Int(f'f_{i}') for i in range(n)]\n\n# Constraint 1: Bijection - each f[i] is in range [0, n-1] and all distinct\nfor i in range(n):\n    solver.add(f[i] >= 0, f[i] < n)\nsolver.add(Distinct(f))\n\n# Build adjacency sets for quick lookup\ng1_adj = set()\nfor u, v in g1_edges:\n    g1_adj.add((min(u,v), max(u,v)))\n\ng2_adj = set()\nfor u, v in g2_edges:\n    g2_adj.add((min(u,v), max(u,v)))\n\n# Constraint 2: Adjacency preservation - for all edges (u,v) in G1, (f(u),f(v)) must be an edge in G2\nfor u, v in g1_edges:\n    # (f[u], f[v]) must be an edge in G2\n    edge_constraints = []\n    for a, b in g2_adj:\n        edge_constraints.append(Or(And(f[u] == a, f[v] == b), And(f[u] == b, f[v] == a)))\n    solver.add(Or(edge_constraints))\n\n# Constraint 3: Reverse preservation - for all edges (a,b) in G2, there must be an edge (u,v) in G1 with f(u)=a, f(v)=b\nfor a, b in g2_adj:\n    edge_constraints = []\n    for u, v in g1_adj:\n        edge_constraints.append(Or(And(f[u] == a, f[v] == b), And(f[u] == b, f[v] == a)))\n    solver.add(Or(edge_constraints))\n\n# Check satisfiability\nBENCHMARK_MODE = True\nresult = solver.check()\n\nif result == sat:\n    model = solver.model()\n    mapping = {}\n    for i in range(n):\n        g2_val = model.evaluate(f[i]).as_long()\n        mapping[str(i)] = g2_names[g2_val]\n    \n    # Build preserved edges\n    preserved = []\n    for u, v in g1_edges:\n        fu = model.evaluate(f[u]).as_long()\n        fv = model.evaluate(f[v]).as_long()\n        preserved.append([f\"{u},{v}\", f\"{g2_names[fu]},{g2_names[fv]}\"])\n    \n    print(\"STATUS: sat\")\n    print(f\"is_isomorphic: True\")\n    print(f\"mapping: {mapping}\")\n    print(f\"preserved_edges: {preserved}\")\n    \nelif result == unsat:\n    print(\"STATUS: unsat\")\n    print(\"is_isomorphic: False\")\n    print(\"mapping: null\")\n    print(\"preserved_edges: []\")\n    if BENCHMARK_MODE:\n        print(\"RAW_RESULT: unsat (semantic/modeling error in benchmark mode; refine required)\")\nelse:\n    print(\"STATUS: unknown\")\n"
}

#### Result

[{'type': 'text', 'text': '{"status":"success","stdout":"STATUS: sat\\r\\nis_isomorphic: True\\r\\nmapping: {\'0\': \'a\', \'1\': \'b\', \'2\': \'c\', \'3\': \'d\', \'4\': \'e\'}\\r\\npreserved_edges: [[\'0,1\', \'a,b\'], [\'0,2\', \'a,c\'], [\'1,3\', \'b,d\'], [\'2,4\', \'c,e\'], [\'3,4\', \'d,e\']]\\r\\n","stderr":null}', 'id': 'lc_a094f3cf-49ad-49e5-8c42-829404805be4'}]


## Iteration 2


```json
{
  "is_isomorphic": true,
  "mapping": {"0": "a", "1": "b", "2": "c", "3": "d", "4": "e"},
  "preserved_edges": [["0,1", "a,b"], ["0,2", "a,c"], ["1,3", "b,d"], ["2,4", "c,e"], ["3,4", "d,e"]]
}
```

### TOKEN USAGE - Iteration 2

  Input tokens:  1,085
  Output tokens: 100
  Total tokens:  1,185

TOKEN USAGE SUMMARY
  Total input tokens:  7,650
  Total output tokens: 968
  Total tokens:        8,618

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
