# Benchmark Report (MCP): ASPBench - 28_graph_isomorphism_hard

**Provider:** mistral2
**Model:** mistral-small-2603
**Solver:** clingo
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: none
**Duration:** 19.32s


 MCP CLINGO AGENT - Symbolic Reasoning

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

  - write_and_run_clingo: Write ASP code to a file for Clingo, validate syntax, and immediately run it to get answer sets.

## Iteration 1


### Phase 1: Analyze & Model

#### Entities and Predicates
1. **Vertices and Colors**:
   - `vertex1(V)`: Vertices in G1.
   - `vertex2(V)`: Vertices in G2.
   - `red1(V)`: Red vertices in G1.
   - `blue1(V)`: Blue vertices in G1.
   - `red2(V)`: Red vertices in G2.
   - `blue2(V)`: Blue vertices in G2.

2. **Special Vertices**:
   - `special1(V)`: Special vertices in G1.
   - `special2(V)`: Special vertices in G2.

3. **Edges and Weights**:
   - `edge1(U, V, W)`: Undirected edge in G1 with weight W.
   - `edge2(U, V, W)`: Undirected edge in G2 with weight W.

4. **Mapping**:
   - `mapping(V1, V2)`: Maps vertex V1 in G1 to vertex V2 in G2.
   - `bijective`: Ensures the mapping is bijective (one-to-one and onto).

5. **Constraints**:
   - `color_preserved(V1, V2)`: Color of V1 in G1 matches color of V2 in G2.
   - `special_preserved(V1, V2)`: Special status of V1 in G1 matches V2 in G2.
   - `edge_preserved(U1, V1, U2, V2, W)`: Edge (U1,V1) with weight W in G1 maps to edge (U2,V2) with weight W in G2.
   - `no_forbidden_triangle`: Ensures no 3-cycle involving a special vertex with total edge weight 60 exists in G2 under the mapping.

6. **Output**:
   - `is_isomorphic`: Boolean indicating if graphs are isomorphic.
   - `mapping(V1, V2)`: The actual mapping (if exists).
   - `preserved_weighted_edges(E1, E2)`: List of edge pairs preserved under the mapping.

#### Domain Grounding
- Vertices for G1: `1..8`
- Vertices for G2: `a,b,c,d,e,f,g,h`
- Colors: `red`, `blue`
- Special vertices: `1` for G1, `a` for G2

#### Constraints
1. **Bijection**: The mapping must be a bijection between G1 and G2 vertices.
2. **Color Preservation**: If `V1` is red in G1, then `V2 = mapping(V1)` must be red in G2, and similarly for blue.
3. **Special Vertex Preservation**: If `V1` is special in G1, then `V2 = mapping(V1)` must be special in G2, and vice versa.
4. **Edge and Weight Preservation**: For every edge `(U1, V1, W)` in G1, there must be an edge `(U2, V2, W)` in G2 where `U2 = mapping(U1)` and `V2 = mapping(V1)`, and vice versa.
5. **Forbidden Subgraph**: No 3-cycle (triangle) in G2 involving a special vertex with total edge weight exactly 60.

#### Forbidden Triangle Check
- A 3-cycle involving a special vertex `S` in G2 means there exist vertices `A` and `B` such that:
  - `(S, A, W1)`, `(S, B, W2)`, and `(A, B, W3)` are edges in G2.
  - `W1 + W2 + W3 = 60`.
- We must ensure that no such triangle exists in G2 under the mapping.

---

### Phase 2: Design and Write ASP Code

#### ASP Code Structure
1. **Facts**: Encode the graph data (vertices, colors, special vertices, edges).
2. **Choice Rule**: Generate possible mappings.
3. **Constraints**:
   - Ensure the mapping is bijective.
   - Enforce color and special vertex preservation.
   - Enforce edge and weight preservation.
   - Forbid forbidden triangles.
4. **Output**:
   - `is_isomorphic`: Derived as `true` if a valid mapping exists.
   - `mapping(V1, V2)`: The actual mapping.
   - `preserved_weighted_edges(E1, E2)`: List of preserved edges.

#### Key ASP Patterns
- **Bijection**: Use `1 { mapping(V1, V2) : vertex2(V2) } 1 :- vertex1(V1).` and `1 { mapping(V1, V2) : vertex1(V1) } 1 :- vertex2(V2).`
- **Color Preservation**: `:- red1(V1), mapping(V1, V2), not red2(V2).` and `:- blue1(V1), mapping(V1, V2), not blue2(V2).`
- **Special Vertex Preservation**: `:- special1(V1), mapping(V1, V2), not special2(V2).` and `:- special2(V2), not special1(V1), mapping(V1, V2).`
- **Edge Preservation**: For every edge in G1, ensure the mapped edge exists in G2 with the same weight, and vice versa.
- **Forbidden Triangle**: Use a constraint to forbid any 3-cycle involving a special vertex with total weight 60.

---

### Phase 3: Write and Run ASP Code

Let's write the ASP code accordingly.

### TOKEN USAGE - Iteration 1

  Input tokens:  6,683
  Output tokens: 2,256
  Total tokens:  8,939

### Tool Call: write_and_run_clingo

  Args: {
  "filename": "graph_isomorphism.lp",
  "code": "% --- Graph G1 ---\nvertex1(1..8).\n\nred1(1;2;5;6).\nblue1(3;4;7;8).\n\nspecial1(1).\n\nedge1(1,3,10). edge1(3,1,10).\nedge1(1,4,20). edge1(4,1,20).\nedge1(2,3,20). edge1(3,2,20).\nedge1(2,4,10). edge1(4,2,10).\n\nedge1(5,7,10). edge1(7,5,10).\nedge1(5,8,20). edge1(8,5,20).\nedge1(6,7,20). edge1(7,6,20).\nedge1(6,8,10). edge1(8,6,10).\n\nedge1(1,5,30). edge1(5,1,30).\nedge1(2,6,30). edge1(6,2,30).\nedge1(3,7,40). edge1(7,3,40).\nedge1(4,8,40). edge1(8,4,40).\n\n% --- Graph G2 ---\nvertex2(a;b;c;d;e;f;g;h).\n\nred2(a;b;e;f).\nblue2(c;d;g;h).\n\nspecial2(a).\n\nedge2(a,c,10). edge2(c,a,10).\nedge2(a,d,20). edge2(d,a,20).\nedge2(b,c,20). edge2(c,b,20).\nedge2(b,d,10). edge2(d,b,10).\n\nedge2(e,g,10). edge2(g,e,10).\nedge2(e,h,20). edge2(h,e,20).\nedge2(f,g,20). edge2(g,f,20).\nedge2(f,h,10). edge2(h,f,10).\n\nedge2(a,e,30). edge2(e,a,30).\nedge2(b,f,30). edge2(f,b,30).\nedge2(c,g,40). edge2(g,c,40).\nedge2(d,h,40). edge2(h,d,40).\n\n% --- Mapping ---\n% Generate possible mappings\n1 { mapping(V1, V2) : vertex2(V2) } 1 :- vertex1(V1).\n1 { mapping(V1, V2) : vertex1(V1) } 1 :- vertex2(V2).\n\n% --- Constraints ---\n% Color preservation\n:- vertex1(V1), red1(V1), mapping(V1, V2), not red2(V2).\n:- vertex1(V1), blue1(V1), mapping(V1, V2), not blue2(V2).\n\n% Special vertex preservation\n:- vertex1(V1), special1(V1), mapping(V1, V2), not special2(V2).\n:- vertex2(V2), special2(V2), not special1(V1), mapping(V1, V2).\n\n% Edge and weight preservation\n:- edge1(U1, V1, W), mapping(U1, U2), mapping(V1, V2),\n   not edge2(U2, V2, W), not edge2(V2, U2, W).\n:- edge2(U2, V2, W), not edge1(U1, V1, W),\n   mapping(U1, U2), mapping(V1, V2).\n\n% Forbidden triangle: no 3-cycle involving a special vertex with total weight 60\n:- special2(S),\n   edge2(S, A, W1), edge2(A, S, W1),\n   edge2(S, B, W2), edge2(B, S, W2),\n   edge2(A, B, W3), edge2(B, A, W3),\n   W1 + W2 + W3 = 60.\n\n% --- Output ---\nis_isomorphic :- mapping(_, _).\n\n% Show the mapping and isomorphism result\n#show mapping/2.\n#show is_isomorphic/0."
}

#### Result

[{'type': 'text', 'text': '{"status":"satisfiable","command":"clingo graph_isomorphism.lp 10 --outf=2 --time-limit=60","models":[["is_isomorphic","mapping(1,a)","mapping(2,b)","mapping(3,c)","mapping(4,d)","mapping(5,e)","mapping(6,f)","mapping(7,g)","mapping(8,h)"]]}', 'id': 'lc_23136679-8a85-4806-84fb-270fe2bae50c'}]


## Iteration 2


{"is_isomorphic": true, "mapping": {"1": "a", "2": "b", "3": "c", "4": "d", "5": "e", "6": "f", "7": "g", "8": "h"}, "preserved_weighted_edges": [ [["1", "3", 10], ["a", "c", 10]], [["1", "4", 20], ["a", "d", 20]], [["1", "5", 30], ["a", "e", 30]], [["2", "3", 20], ["b", "c", 20]], [["2", "4", 10], ["b", "d", 10]], [["2", "6", 30], ["b", "f", 30]], [["3", "7", 40], ["c", "g", 40]], [["4", "8", 40], ["d", "h", 40]], [["5", "7", 10], ["e", "g", 10]], [["5", "8", 20], ["e", "h", 20]], [["6", "7", 20], ["f", "g", 20]], [["6", "8", 10], ["f", "h", 10]] ]}

### TOKEN USAGE - Iteration 2

  Input tokens:  1,648
  Output tokens: 322
  Total tokens:  1,970

TOKEN USAGE SUMMARY
  Total input tokens:  8,331
  Total output tokens: 2,578
  Total tokens:        10,909

COMPLETE

## Final Answer

```json
{"is_isomorphic": true, "mapping": {"1": "a", "2": "b", "3": "c", "4": "d", "5": "e", "6": "f", "7": "g", "8": "h"}, "preserved_weighted_edges": [ [["1", "3", 10], ["a", "c", 10]], [["1", "4", 20], ["a", "d", 20]], [["1", "5", 30], ["a", "e", 30]], [["2", "3", 20], ["b", "c", 20]], [["2", "4", 10], ["b", "d", 10]], [["2", "6", 30], ["b", "f", 30]], [["3", "7", 40], ["c", "g", 40]], [["4", "8", 40], ["d", "h", 40]], [["5", "7", 10], ["e", "g", 10]], [["5", "8", 20], ["e", "h", 20]], [["6", "7", 20], ["f", "g", 20]], [["6", "8", 10], ["f", "h", 10]] ]}
```
