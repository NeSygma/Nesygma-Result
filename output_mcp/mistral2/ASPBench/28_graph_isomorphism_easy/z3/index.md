# Benchmark Report (MCP): ASPBench - 28_graph_isomorphism_easy

**Provider:** mistral2
**Model:** mistral-small-2603
**Solver:** z3
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: none
**Duration:** 26.00s


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


### Phase 1: Analyze & Model

**Entities and Variables:**
- **Graph 1 (G1):**
  - Vertices: `0, 1, 2, 3, 4`
  - Edges: `(0,1)`, `(0,2)`, `(1,3)`, `(2,4)`, `(3,4)`
- **Graph 2 (G2):**
  - Vertices: `a, b, c, d, e`
  - Edges: `(a,b)`, `(a,c)`, `(b,d)`, `(c,e)`, `(d,e)`

**Constraints:**
1. **Bijection**: A one-to-one and onto mapping from `G1` vertices to `G2` vertices.
2. **Adjacency Preservation**: For every edge `(u,v)` in `G1`, the edge `(f(u), f(v))` must exist in `G2`.
3. **Reverse Preservation**: For every edge `(x,y)` in `G2`, the edge `(f⁻¹(x), f⁻¹(y))` must exist in `G1`.
4. **Degree Preservation**: The degree of each vertex in `G1` must match the degree of its mapped vertex in `G2`.

**Objective:**
- Determine if a bijection `f` exists such that all constraints are satisfied.
- If it exists, output the mapping and the preserved edges.

---

### Phase 2: Design and Write

**Approach:**
1. **Bijection**: Use a list of Z3 `Int` variables to represent the mapping from `G1` vertices to `G2` vertices. Ensure the mapping is bijective by enforcing:
   - All mapped values are distinct (injective).
   - All `G2` vertices are covered (surjective).
2. **Adjacency Preservation**: For each edge `(u,v)` in `G1`, check that `(f(u), f(v))` is an edge in `G2`.
3. **Reverse Preservation**: For each edge `(x,y)` in `G2`, check that `(f⁻¹(x), f⁻¹(y))` is an edge in `G1`. This can be done by ensuring that for every edge `(x,y)` in `G2`, the pair `(f⁻¹(x), f⁻¹(y))` is an edge in `G1`.
4. **Degree Preservation**: Precompute the degree of each vertex in `G1` and `G2`. Ensure that for each vertex `u` in `G1`, the degree of `u` equals the degree of `f(u)` in `G2`.

**Implementation Details:**
- Represent `G1` and `G2` vertices as integers for easier indexing.
- Use Z3 `Int` variables for the mapping.
- Use Z3 `Solver` to check for satisfiability.
- If a model is found, extract the mapping and the preserved edges.

---

### Phase 3: Write and Run

```python
from z3 import *

# Define the vertices for G1 and G2
G1_vertices = [0, 1, 2, 3, 4]
G2_vertices = ['a', 'b', 'c', 'd', 'e']

# Map G2 vertices to integers for easier indexing
G2_vertex_to_int = {v: i for i, v in enumerate(G2_vertices)}
G2_int_to_vertex = {i: v for i, v in enumerate(G2_vertices)}

# Define edges for G1 and G2
G1_edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4)]
G2_edges = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'e'), ('d', 'e')]

# Compute degrees for G1 and G2
def compute_degrees(vertices, edges):
    degree = {v: 0 for v in vertices}
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1
    return degree

G1_degree = compute_degrees(G1_vertices, G1_edges)
G2_degree = compute_degrees(G2_vertices, G2_edges)

# Create a solver
solver = Solver()

# Declare the mapping from G1 vertices to G2 vertices (as integers)
mapping = [Int(f'mapping_{i}') for i in G1_vertices]

# Constraint 1: Bijection (injective and surjective)
# Injective: All mapped values are distinct
solver.add(Distinct(mapping))

# Surjective: All G2 vertices are covered
# Since the domain and codomain are the same size (5), injective implies surjective
# So we only need to ensure the mapping is injective

# Constraint 2: Adjacency preservation
for u, v in G1_edges:
    # For edge (u,v) in G1, (mapping[u], mapping[v]) must be an edge in G2
    # We need to check if (mapping[u], mapping[v]) is in G2_edges
    # Since G2_edges are tuples of strings, we need to convert the mapped integers back to strings
    solver.add(
        Or(
            And(
                mapping[u] == G2_vertex_to_int['a'],
                mapping[v] == G2_vertex_to_int['b']
            ),
            And(
                mapping[u] == G2_vertex_to_int['a'],
                mapping[v] == G2_vertex_to_int['c']
            ),
            And(
                mapping[u] == G2_vertex_to_int['b'],
                mapping[v] == G2_vertex_to_int['d']
            ),
            And(
                mapping[u] == G2_vertex_to_int['c'],
                mapping[v] == G2_vertex_to_int['e']
            ),
            And(
                mapping[u] == G2_vertex_to_int['d'],
                mapping[v] == G2_vertex_to_int['e']
            ),
            And(
                mapping[u] == G2_vertex_to_int['b'],
                mapping[v] == G2_vertex_to_int['a']
            ),
            And(
                mapping[u] == G2_vertex_to_int['c'],
                mapping[v] == G2_vertex_to_int['a']
            ),
            And(
                mapping[u] == G2_vertex_to_int['d'],
                mapping[v] == G2_vertex_to_int['b']
            ),
            And(
                mapping[u] == G2_vertex_to_int['e'],
                mapping[v] == G2_vertex_to_int['c']
            ),
            And(
                mapping[u] == G2_vertex_to_int['e'],
                mapping[v] == G2_vertex_to_int['d']
            )
        )
    )

# Constraint 3: Reverse adjacency preservation
# For every edge (x,y) in G2, (f⁻¹(x), f⁻¹(y)) must be an edge in G1
# To implement this, we need to ensure that for every edge (x,y) in G2,
# there exists a pair (u,v) in G1 such that mapping[u] = x and mapping[v] = y
for x, y in G2_edges:
    # Check if there exists u, v in G1 such that mapping[u] = G2_vertex_to_int[x] and mapping[v] = G2_vertex_to_int[y]
    # and (u,v) is an edge in G1
    solver.add(
        Or(
            And(
                Or([mapping[u] == G2_vertex_to_int[x] for u in G1_vertices]),
                Or([mapping[v] == G2_vertex_to_int[y] for v in G1_vertices]),
                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])
            )
        )
    )

# Constraint 4: Degree preservation
for u in G1_vertices:
    solver.add(
        Or(
            And(
                mapping[u] == G2_vertex_to_int['a'],
                G1_degree[u] == G2_degree['a']
            ),
            And(
                mapping[u] == G2_vertex_to_int['b'],
                G1_degree[u] == G2_degree['b']
            ),
            And(
                mapping[u] == G2_vertex_to_int['c'],
                G1_degree[u] == G2_degree['c']
            ),
            And(
                mapping[u] == G2_vertex_to_int['d'],
                G1_degree[u] == G2_degree['d']
            ),
            And(
                mapping[u] == G2_vertex_to_int['e'],
                G1_degree[u] == G2_degree['e']
            )
        )
    )

# Check if the graphs are isomorphic
result = solver.check()

if result == sat:
    model = solver.model()
    # Extract the mapping
    mapping_dict = {}
    for u in G1_vertices:
        mapped_val = model[mapping[u]]
        # Convert the integer back to the G2 vertex
        for v, i in G2_vertex_to_int.items():
            if i == mapped_val:
                mapping_dict[u] = v
                break

    # Extract preserved edges
    preserved_edges = []
    for u, v in G1_edges:
        mapped_u = mapping_dict[u]
        mapped_v = mapping_dict[v]
        preserved_edges.append([f"{u},{v}", f"{mapped_u},{mapped_v}"])

    print("STATUS: sat")
    print("is_isomorphic = True")
    print("mapping =", mapping_dict)
    print("preserved_edges =", preserved_edges)
elif result == unsat:
    print("STATUS: unsat")
    print("is_isomorphic = False")
    print("mapping = null")
    print("preserved_edges = []")
else:
    print("STATUS: unknown")
```

### TOKEN USAGE - Iteration 1

  Input tokens:  6,624
  Output tokens: 4,511
  Total tokens:  11,135

### Tool Call: write_and_run_z3

  Args: {
  "filename": "graph_isomorphism.py",
  "code": "from z3 import *\n\n# Define the vertices for G1 and G2\nG1_vertices = [0, 1, 2, 3, 4]\nG2_vertices = ['a', 'b', 'c', 'd', 'e']\n\n# Map G2 vertices to integers for easier indexing\nG2_vertex_to_int = {v: i for i, v in enumerate(G2_vertices)}\nG2_int_to_vertex = {i: v for i, v in enumerate(G2_vertices)}\n\n# Define edges for G1 and G2\nG1_edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 4)]\nG2_edges = [('a', 'b'), ('a', 'c'), ('b', 'd'), ('c', 'e'), ('d', 'e')]\n\n# Compute degrees for G1 and G2\ndef compute_degrees(vertices, edges):\n    degree = {v: 0 for v in vertices}\n    for u, v in edges:\n        degree[u] += 1\n        degree[v] += 1\n    return degree\n\nG1_degree = compute_degrees(G1_vertices, G1_edges)\nG2_degree = compute_degrees(G2_vertices, G2_edges)\n\n# Create a solver\nsolver = Solver()\n\n# Declare the mapping from G1 vertices to G2 vertices (as integers)\nmapping = [Int(f'mapping_{i}') for i in G1_vertices]\n\n# Constraint 1: Bijection (injective and surjective)\n# Injective: All mapped values are distinct\nsolver.add(Distinct(mapping))\n\n# Constraint 2: Adjacency preservation\nfor u, v in G1_edges:\n    # For edge (u,v) in G1, (mapping[u], mapping[v]) must be an edge in G2\n    # We need to check if (mapping[u], mapping[v]) is in G2_edges\n    # Since G2_edges are tuples of strings, we need to convert the mapped integers back to strings\n    solver.add(\n        Or(\n            And(\n                mapping[u] == G2_vertex_to_int['a'],\n                mapping[v] == G2_vertex_to_int['b']\n            ),\n            And(\n                mapping[u] == G2_vertex_to_int['a'],\n                mapping[v] == G2_vertex_to_int['c']\n            ),\n            And(\n                mapping[u] == G2_vertex_to_int['b'],\n                mapping[v] == G2_vertex_to_int['d']\n            ),\n            And(\n                mapping[u] == G2_vertex_to_int['c'],\n                mapping[v] == G2_vertex_to_int['e']\n            ),\n            And(\n                mapping[u] == G2_vertex_to_int['d'],\n                mapping[v] == G2_vertex_to_int['e']\n            ),\n            And(\n                mapping[u] == G2_vertex_to_int['b'],\n                mapping[v] == G2_vertex_to_int['a']\n            ),\n            And(\n                mapping[u] == G2_vertex_to_int['c'],\n                mapping[v] == G2_vertex_to_int['a']\n            ),\n            And(\n                mapping[u] == G2_vertex_to_int['d'],\n                mapping[v] == G2_vertex_to_int['b']\n            ),\n            And(\n                mapping[u] == G2_vertex_to_int['e'],\n                mapping[v] == G2_vertex_to_int['c']\n            ),\n            And(\n                mapping[u] == G2_vertex_to_int['e'],\n                mapping[v] == G2_vertex_to_int['d']\n            )\n        )\n    )\n\n# Constraint 3: Reverse adjacency preservation\n# For every edge (x,y) in G2, (f\u207b\u00b9(x), f\u207b\u00b9(y)) must be an edge in G1\n# To implement this, we need to ensure that for every edge (x,y) in G2,\n# there exists a pair (u,v) in G1 such that mapping[u] = x and mapping[v] = y\nfor x, y in G2_edges:\n    # Check if there exists u, v in G1 such that mapping[u] = G2_vertex_to_int[x] and mapping[v] = G2_vertex_to_int[y]\n    # and (u,v) is an edge in G1\n    solver.add(\n        Or(\n            And(\n                mapping[0] == G2_vertex_to_int[x],\n                mapping[1] == G2_vertex_to_int[y],\n                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])\n            ),\n            And(\n                mapping[0] == G2_vertex_to_int[x],\n                mapping[2] == G2_vertex_to_int[y],\n                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])\n            ),\n            And(\n                mapping[0] == G2_vertex_to_int[x],\n                mapping[3] == G2_vertex_to_int[y],\n                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])\n            ),\n            And(\n                mapping[0] == G2_vertex_to_int[x],\n                mapping[4] == G2_vertex_to_int[y],\n                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])\n            ),\n            And(\n                mapping[1] == G2_vertex_to_int[x],\n                mapping[2] == G2_vertex_to_int[y],\n                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])\n            ),\n            And(\n                mapping[1] == G2_vertex_to_int[x],\n                mapping[3] == G2_vertex_to_int[y],\n                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])\n            ),\n            And(\n                mapping[1] == G2_vertex_to_int[x],\n                mapping[4] == G2_vertex_to_int[y],\n                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])\n            ),\n            And(\n                mapping[2] == G2_vertex_to_int[x],\n                mapping[3] == G2_vertex_to_int[y],\n                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])\n            ),\n            And(\n                mapping[2] == G2_vertex_to_int[x],\n                mapping[4] == G2_vertex_to_int[y],\n                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])\n            ),\n            And(\n                mapping[3] == G2_vertex_to_int[x],\n                mapping[4] == G2_vertex_to_int[y],\n                Or([And(mapping[u] == G2_vertex_to_int[x], mapping[v] == G2_vertex_to_int[y]) for u, v in G1_edges])\n            )\n        )\n    )\n\n# Constraint 4: Degree preservation\nfor u in G1_vertices:\n    solver.add(\n        Or(\n            And(\n                mapping[u] == G2_vertex_to_int['a'],\n                G1_degree[u] == G2_degree['a']\n            ),\n            And(\n                mapping[u] == G2_vertex_to_int['b'],\n                G1_degree[u] == G2_degree['b']\n            ),\n            And(\n                mapping[u] == G2_vertex_to_int['c'],\n                G1_degree[u] == G2_degree['c']\n            ),\n            And(\n                mapping[u] == G2_vertex_to_int['d'],\n                G1_degree[u] == G2_degree['d']\n            ),\n            And(\n                mapping[u] == G2_vertex_to_int['e'],\n                G1_degree[u] == G2_degree['e']\n            )\n        )\n    )\n\n# Check if the graphs are isomorphic\nresult = solver.check()\n\nif result == sat:\n    model = solver.model()\n    # Extract the mapping\n    mapping_dict = {}\n    for u in G1_vertices:\n        mapped_val = model[mapping[u]]\n        # Convert the integer back to the G2 vertex\n        for v, i in G2_vertex_to_int.items():\n            if i == mapped_val:\n                mapping_dict[u] = v\n                break\n\n    # Extract preserved edges\n    preserved_edges = []\n    for u, v in G1_edges:\n        mapped_u = mapping_dict[u]\n        mapped_v = mapping_dict[v]\n        preserved_edges.append([f\"{u},{v}\", f\"{mapped_u},{mapped_v}\"])\n\n    print(\"STATUS: sat\")\n    print(\"is_isomorphic = True\")\n    print(\"mapping =\", mapping_dict)\n    print(\"preserved_edges =\", preserved_edges)\nelif result == unsat:\n    print(\"STATUS: unsat\")\n    print(\"is_isomorphic = False\")\n    print(\"mapping = null\")\n    print(\"preserved_edges = []\")\nelse:\n    print(\"STATUS: unknown\")"
}

#### Result

[{'type': 'text', 'text': '{"status":"success","stdout":"STATUS: sat\\r\\nis_isomorphic = True\\r\\nmapping = {0: \'a\', 1: \'b\', 2: \'c\', 3: \'d\', 4: \'e\'}\\r\\npreserved_edges = [[\'0,1\', \'a,b\'], [\'0,2\', \'a,c\'], [\'1,3\', \'b,d\'], [\'2,4\', \'c,e\'], [\'3,4\', \'d,e\']]\\r\\n","stderr":null}', 'id': 'lc_688753e2-9138-4510-9f18-e6afb691407f'}]


## Iteration 2


{"is_isomorphic": true, "mapping": {"0": "a", "1": "b", "2": "c", "3": "d", "4": "e"}, "preserved_edges": [["0,1", "a,b"], ["0,2", "a,c"], ["1,3", "b,d"], ["2,4", "c,e"], ["3,4", "d,e"]]}

### TOKEN USAGE - Iteration 2

  Input tokens:  1,115
  Output tokens: 94
  Total tokens:  1,209

TOKEN USAGE SUMMARY
  Total input tokens:  7,739
  Total output tokens: 4,605
  Total tokens:        12,344

COMPLETE

## Final Answer

```json
{"is_isomorphic": true, "mapping": {"0": "a", "1": "b", "2": "c", "3": "d", "4": "e"}, "preserved_edges": [["0,1", "a,b"], ["0,2", "a,c"], ["1,3", "b,d"], ["2,4", "c,e"], ["3,4", "d,e"]]}
```
