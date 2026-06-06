# Benchmark Report (MCP): ASPBench - 28_graph_isomorphism_easy

**Provider:** openrouter
**Model:** openai/gpt-oss-120b
**Solver:** clingo
**Config:** max_output_tokens: 32768, temperature: 0.0, top_p: 1.0, seed: 42, reasoning_enabled: True, reasoning_effort: medium
**Duration:** 39.61s


 MCP CLINGO AGENT - Symbolic Reasoning

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

  - write_and_run_clingo: Write ASP code to a file for Clingo, validate syntax, and immediately run it to get answer sets.

## Iteration 1



### Thinking

- We need to translate to ASP and output solution. Need to produce code that determines isomorphism and outputs mapping and preserved edges. Must follow guidelines: produce ASP code with #show directives for answer. Since it's a decision problem, we can output answer(true/false) etc. But the problem expects fields: is_isomorphic boolean, mapping object, preserved_edges array. However we must output ASP code only. The downstream will synthesize answer. So we need to encode the problem and produce answer atoms.
- We need to output mapping if exists. Could output mapping(V1,V2) atoms. Also maybe isomorphic atom.
- We need to ensure unique solution? Graph isomorphism may have multiple bijections. The problem expects maybe any mapping. But guidelines: if multiple models, need refine to ensure unique definitive solution. So we must enforce uniqueness: maybe enforce ordering to pick lexicographically smallest mapping? Could add optimization to minimize something, but we can also add constraints to enforce a canonical mapping: e.g., map vertex 0 to the smallest label (alphabetically) among possible matches. But we need deterministic unique answer.
- Simpler: we can add a rule to select exactly one bijection and then use #show to output mapping and isomorphic. But multiple bijections will cause multiple answer sets. That violates requirement: must have unique solution. So we need to enforce a single mapping, perhaps by adding a total order and requiring mapping to be the lexicographically smallest based on vertex ordering.
- We can encode a total order on G2 vertices: a<b<c<d<e. Then enforce that mapping respects order: if u<v then f(u) < f(v) according to order. This will enforce a unique monotone bijection if exists. However graph may not have monotone mapping; but if there is any isomorphism, there may be one that respects order? Not necessarily. For arbitrary graphs, monotone mapping may not exist. So this could incorrectly deem unsat.
- Alternative: use optimization to minimize a tuple of mapped vertices in order to pick smallest mapping. Use #minimize with tuple: we can minimize sum of indices of mapped G2 vertices weighted by powers. But we need to assign numeric IDs to G2 vertices: a=0,b=1,c=2,d=3,e=4. Then minimize sum of f(u)*5^(max-u) to get lexicographically smallest. Simpler: minimize total sum of mapped indices; but multiple bijections could have same sum. Could also minimize lexicographically using #minimize with tuple list: #minimize { (Idx, U) : map(U,V), idx(V,Idx) }. Not sure.
- Simpler: we can enforce a deterministic mapping by adding a rule that picks the first possible mapping using choice rule with ordering: use "1 { map(U,V) : vertex2(V) } 1 :- vertex1(U)." This generates many bijections. Then we can add a constraint to enforce that the mapping is the lexicographically smallest: we can use ":- map(U,V), map(U,W), V < W." but that's already bijection.
- To enforce uniqueness, we can add a rule that selects exactly one answer set via #show only mapping and isomorphic, but multiple answer sets still exist. The guidelines say if more than 1 model, refine to ensure unique solution. So we need to ensure exactly one model.
- We can use #show and also add a #show for a sentinel and then use #minimize to get optimal model. Clingo returns optimal model(s) maybe multiple if same optimum. Could add #minimize with lexicographic priority to break ties: use #minimize { 1, V : map(0,V) }. Actually we can minimize the tuple of mapped vertices for vertex 0, then vertex1, etc. Use #minimize with multiple levels: #minimize { 1, V : map(0,V) }. #minimize { 2, V : map(1,V) }. etc. This will prioritize lower level first? In clingo, lower priority numbers are higher priority? Actually #minimize { weight, tuple } with @level. Use @level to set priority. So we can do #minimize { 1, V : map(0,V) } @1. #minimize { 1, V : map(1,V) } @2 etc. This will find model minimizing V for vertex0, then vertex1, etc. That yields unique minimal mapping.
- Thus we can produce unique solution.
- Now encode graphs.
- Define vertex1(0..4). vertex2(a..e). Use constants: a,b,c,d,e as strings need quotes? They start with lowercase letters, okay.
- Define edge1(u,v) for undirected edges. We'll store both directions for adjacency check.
- Similarly edge2.
- Define adjacency predicate adj1(U,V) :- edge1(U,V). Also symmetric: edge1 defined both ways.
- We'll define edge1(0,1). edge1(1,0). etc.
- Now bijection: 1 { map(U,V) : vertex2(V) } 1 :- vertex1(U). Ensure each U maps to exactly one V.
- Injectivity: ensure no two U map to same V: :- map(U,V), map(W,V), U != W.
- Adjacency preservation: For each edge1(U,V) (undirected), require edge2(FU,FV). So constraint: :- edge1(U,V), map(U, FU), map(V, FV), not edge2(FU,FV).
- Similarly reverse: :- edge2(X,Y), map_inv? We need to ensure that for each edge2, there is edge1 between preimages. So we need inverse mapping: map(U,V) implies invmap(V,U). We can define invmap(V,U) :- map(U,V). Then constraint: :- edge2(X,Y), invmap(X,U), invmap(Y,V), not edge1(U,V).
- Degree preservation: compute degree1(U) = #count{V : edge1(U,V)}. degree2(V) similarly. Then enforce degree equality: :- map(U,V), degree1(U) != degree2(V). Use aggregate.
- Now define isomorphic atom if mapping exists and constraints satisfied. Since constraints already enforce, any model will satisfy. So we can define isomorphic :- not conflict? Actually if constraints are satisfied, model exists. So we can just #show isomorphic if mapping exists. Define isomorphic :- map(_, _). But that will be true always if any mapping exists. Since constraints ensure bijection, we can define isomorphic :- map(0, _). (any mapping). Or simply define isomorphic.
- Now we need to output mapping pairs. Use #show map/2.
- Also output preserved_edges: we can define preserved(U,V) :- edge1(U,V), map(U,FU), map(V,FV), edge2(FU,FV). Then #show preserved/2.
- But need to output as pairs "u,v" "f(u),f(v)". However we just output atoms; downstream can format.
- Now ensure unique model via #minimize.
- Define idx2(V,Idx) facts: idx2(a,0). idx2(b,1). idx2(c,2). idx2(d,3). idx2(e,4).
- Now #minimize { 1, Idx : map(0,V), idx2(V,Idx) } @1. #minimize { 1, Idx : map(1,V), idx2(V,Idx) } @2. ... up to vertex4.
- This will pick smallest possible mapping lexicographically.
- Now we need to ensure that the program is safe and all predicates appear in heads.
- Define vertex1(0..4). vertex2(a;b;c;d;e). Use facts.
- Define edge1 and edge2 both directions.
- Define degree1(U,N) :- N = #count{V : edge1(U,V)}. Similarly degree2.
- Now constraints.
- Now #show directives: #show isomorphic/0. #show map/2. #show preserved/2.
- Now run.
- Let's craft code.




### TOKEN USAGE - Iteration 1

  Input tokens:  6,259
  Output tokens: 2,426
  Total tokens:  8,685

### Tool Call: write_and_run_clingo

  Args: {
  "code": "% Vertices of G1\nvertex1(0). vertex1(1). vertex1(2). vertex1(3). vertex1(4).\n% Vertices of G2\nvertex2(a). vertex2(b). vertex2(c). vertex2(d). vertex2(e).\n% Index for ordering G2 vertices\nidx2(a,0). idx2(b,1). idx2(c,2). idx2(d,3). idx2(e,4).\n% Edges of G1 (undirected, both directions)\nedge1(0,1). edge1(1,0).\nedge1(0,2). edge1(2,0).\nedge1(1,3). edge1(3,1).\nedge1(2,4). edge1(4,2).\nedge1(3,4). edge1(4,3).\n% Edges of G2 (undirected)\nedge2(a,b). edge2(b,a).\nedge2(a,c). edge2(c,a).\nedge2(b,d). edge2(d,b).\nedge2(c,e). edge2(e,c).\nedge2(d,e). edge2(e,d).\n% Bijection: each vertex of G1 maps to exactly one vertex of G2\n1 { map(U,V) : vertex2(V) } 1 :- vertex1(U).\n% Injectivity: no two G1 vertices map to same G2 vertex\n:- map(U,V), map(W,V), U != W.\n% Inverse mapping helper\ninvmap(V,U) :- map(U,V).\n% Degree computation\ndeg1(U,N) :- vertex1(U), N = #count { V : edge1(U,V) }.\ndeg2(V,N) :- vertex2(V), N = #count { W : edge2(V,W) }.\n% Degree preservation\n:- map(U,V), deg1(U,D1), deg2(V,D2), D1 != D2.\n% Adjacency preservation (G1 -> G2)\n:- edge1(U,V), map(U,FU), map(V,FV), not edge2(FU,FV).\n% Reverse adjacency preservation (G2 -> G1)\n:- edge2(X,Y), invmap(X,U), invmap(Y,V), not edge1(U,V).\n% Define isomorphic when a bijection satisfying constraints exists\nisomorphic :- map(_, _).\n% Preserve edges for output\npreserved(U,V) :- edge1(U,V), map(U,FU), map(V,FV), edge2(FU,FV).\n% Lexicographically minimal mapping (unique solution)\n#minimize { 1, Idx : map(0,V), idx2(V,Idx) } @1.\n#minimize { 1, Idx : map(1,V), idx2(V,Idx) } @2.\n#minimize { 1, Idx : map(2,V), idx2(V,Idx) } @3.\n#minimize { 1, Idx : map(3,V), idx2(V,Idx) } @4.\n#minimize { 1, Idx : map(4,V), idx2(V,Idx) } @5.\n#show isomorphic/0.\n#show map/2.\n#show preserved/2.\n",
  "filename": "iso.lp"
}

#### Result

[{'type': 'text', 'text': '{"status":"syntax_error","error":"<block>:39:46-47: error: syntax error, unexpected @, expecting .\\n\\n<block>:40:46-47: error: syntax error, unexpected @, expecting .\\n\\n<block>:41:46-47: error: syntax error, unexpected @, expecting .\\n\\n<block>:42:46-47: error: syntax error, unexpected @, expecting .\\n\\n<block>:43:46-47: error: syntax error, unexpected @, expecting .\\n\\nparsing failed","hint":"Fix the ASP syntax. Common issues: missing periods, undefined atoms, variable capitalization."}', 'id': 'lc_26a43fbb-6957-4735-97c1-fc3e9ecea333'}]


## Iteration 2



### Thinking

- The syntax error is due to using @ for priority incorrectly. In Clingo, the syntax is `#minimize { weight, tuple : condition } .` and you can add `@level` after the weight? Actually the syntax is `#minimize { w@l, tuple : condition } .` where `@l` is priority level. The correct syntax: `#minimize { 1@1, Idx : map(0,V), idx2(V,Idx) }.`? Wait weight and priority: `weight@priority`. So we can write `#minimize { Idx@1 : map(0,V), idx2(V,Idx) }.` but we need weight as well. We can set weight 1 and priority level. Actually we want to minimize Idx with priority levels. Use `#minimize { Idx@1 : map(0,V), idx2(V,Idx) }.` This will minimize sum of Idx with priority 1. Then for next vertex, we need higher priority number (lower priority) i.e., larger number? In Clingo, lower priority number is higher priority (i.e., 1 is highest). So we want vertex0 priority 1, vertex1 priority 2, etc. So we can write:
- `#minimize { Idx@1 : map(0,V), idx2(V,Idx) }.`
- `#minimize { Idx@2 : map(1,V), idx2(V,Idx) }.` etc.
- Thus remove weight and use Idx as weight? Actually weight must be integer, can be Idx. That's fine.
- Let's adjust.
- Also need period after each #minimize.
- Let's rewrite code.




### TOKEN USAGE - Iteration 2

  Input tokens:  10,167
  Output tokens: 1,084
  Total tokens:  11,251

### Tool Call: write_and_run_clingo

  Args: {
  "code": "% Vertices of G1\nvertex1(0). vertex1(1). vertex1(2). vertex1(3). vertex1(4).\n% Vertices of G2\nvertex2(a). vertex2(b). vertex2(c). vertex2(d). vertex2(e).\n% Index for ordering G2 vertices\nidx2(a,0). idx2(b,1). idx2(c,2). idx2(d,3). idx2(e,4).\n% Edges of G1 (undirected, both directions)\nedge1(0,1). edge1(1,0).\nedge1(0,2). edge1(2,0).\nedge1(1,3). edge1(3,1).\nedge1(2,4). edge1(4,2).\nedge1(3,4). edge1(4,3).\n% Edges of G2 (undirected)\nedge2(a,b). edge2(b,a).\nedge2(a,c). edge2(c,a).\nedge2(b,d). edge2(d,b).\nedge2(c,e). edge2(e,c).\nedge2(d,e). edge2(e,d).\n% Bijection: each vertex of G1 maps to exactly one vertex of G2\n1 { map(U,V) : vertex2(V) } 1 :- vertex1(U).\n% Injectivity: no two G1 vertices map to same G2 vertex\n:- map(U,V), map(W,V), U != W.\n% Inverse mapping helper\ninvmap(V,U) :- map(U,V).\n% Degree computation\ndeg1(U,N) :- vertex1(U), N = #count { V : edge1(U,V) }.\ndeg2(V,N) :- vertex2(V), N = #count { W : edge2(V,W) }.\n% Degree preservation\n:- map(U,V), deg1(U,D1), deg2(V,D2), D1 != D2.\n% Adjacency preservation (G1 -> G2)\n:- edge1(U,V), map(U,FU), map(V,FV), not edge2(FU,FV).\n% Reverse adjacency preservation (G2 -> G1)\n:- edge2(X,Y), invmap(X,U), invmap(Y,V), not edge1(U,V).\n% Define isomorphic when a bijection satisfying constraints exists\nisomorphic :- map(_, _).\n% Preserve edges for output\npreserved(U,V) :- edge1(U,V), map(U,FU), map(V,FV), edge2(FU,FV).\n% Lexicographically minimal mapping (unique solution)\n#minimize { Idx@1 : map(0,V), idx2(V,Idx) }.\n#minimize { Idx@2 : map(1,V), idx2(V,Idx) }.\n#minimize { Idx@3 : map(2,V), idx2(V,Idx) }.\n#minimize { Idx@4 : map(3,V), idx2(V,Idx) }.\n#minimize { Idx@5 : map(4,V), idx2(V,Idx) }.\n#show isomorphic/0.\n#show map/2.\n#show preserved/2.\n",
  "filename": "iso.lp"
}

#### Result

[{'type': 'text', 'text': '{"status":"optimum_found","command":"clingo iso.lp 10 --outf=2 --time-limit=60","models":[["preserved(1,0)","preserved(2,0)","preserved(0,1)","map(0,a)","preserved(3,1)","preserved(0,2)","map(2,b)","preserved(4,2)","preserved(1,3)","preserved(4,3)","preserved(2,4)","preserved(3,4)","map(1,c)","map(4,d)","map(3,e)","isomorphic"],["preserved(1,0)","map(1,a)","preserved(2,0)","preserved(0,1)","preserved(3,1)","preserved(0,2)","preserved(4,2)","preserved(1,3)","map(3,b)","preserved(4,3)","preserved(2,4)","preserved(3,4)","map(0,c)","map(4,d)","map(2,e)","isomorphic"],["preserved(1,0)","preserved(2,0)","map(2,a)","preserved(0,1)","preserved(3,1)","preserved(0,2)","preserved(4,2)","preserved(1,3)","preserved(4,3)","preserved(2,4)","map(4,b)","preserved(3,4)","map(0,c)","map(3,d)","map(1,e)","isomorphic"],["preserved(1,0)","preserved(2,0)","preserved(0,1)","preserved(3,1)","map(3,a)","preserved(0,2)","preserved(4,2)","preserved(1,3)","preserved(4,3)","preserved(2,4)","map(4,b)","preserved(3,4)","map(1,c)","map(2,d)","map(0,e)","isomorphic"],["preserved(1,0)","preserved(2,0)","preserved(0,1)","preserved(3,1)","preserved(0,2)","preserved(4,2)","map(4,a)","preserved(1,3)","map(3,b)","preserved(4,3)","preserved(2,4)","preserved(3,4)","map(2,c)","map(1,d)","map(0,e)","isomorphic"]]}', 'id': 'lc_c07018ea-a279-4466-8c3b-070f0c37be60'}]


## Iteration 3



### Thinking

- We need to parse solver output. It's JSON with "models": list of models, each a list of atoms. We need to produce final answer JSON with fields is_isomorphic, mapping, preserved_edges.
- We must select the best model among available (first 10). All models have "isomorphic" atom, so is_isomorphic true. Need mapping from model: atoms map(v,w). Choose one model. Probably first model.
- First model atoms: ["preserved(1,0)","preserved(2,0)","preserved(0,1)","map(0,a)","preserved(3,1)","preserved(0,2)","map(2,b)","preserved(4,2)","preserved(1,3)","preserved(4,3)","preserved(2,4)","preserved(3,4)","map(1,c)","map(4,d)","map(3,e)","isomorphic"]
- Mapping: 0 -> a 2 -> b 1 -> c 4 -> d 3 -> e
- We need mapping for all vertices 0-4. Yes.
- Now preserved_edges: need pairs of original edge and mapped edge. Original edges list: (0,1),(0,2),(1,3),(2,4),(3,4). For each, we need to output as strings "u,v" and "f(u),f(v)". Use mapping.
- Compute: 0-1 -> a,c => "0,1","a,c" 0-2 -> a,b => "0,2","a,b" 1-3 -> c,e => "1,3","c,e" 2-4 -> b,d => "2,4","b,d" 3-4 -> e,d => "3,4","e,d"
- Check preserved atoms: they have preserved(0,1) etc. The preserved atoms include (0,1) etc. So mapping matches.
- Now produce JSON:
- { "is_isomorphic": true, "mapping": {"0":"a","1":"c","2":"b","3":"e","4":"d"}, "preserved_edges": [["0,1","a,c"],["0,2","a,b"],["1,3","c,e"],["2,4","b,d"],["3,4","e,d"]] }
- Make sure ordering maybe not required. Provide exactly.


{
  "is_isomorphic": true,
  "mapping": {
    "0": "a",
    "1": "c",
    "2": "b",
    "3": "e",
    "4": "d"
  },
  "preserved_edges": [
    ["0,1", "a,c"],
    ["0,2", "a,b"],
    ["1,3", "c,e"],
    ["2,4", "b,d"],
    ["3,4", "e,d"]
  ]
}

### TOKEN USAGE - Iteration 3

  Input tokens:  1,575
  Output tokens: 626
  Total tokens:  2,201

TOKEN USAGE SUMMARY
  Total input tokens:  18,001
  Total output tokens: 4,136
  Total tokens:        22,137

COMPLETE

## Final Answer

```json
{
  "is_isomorphic": true,
  "mapping": {
    "0": "a",
    "1": "c",
    "2": "b",
    "3": "e",
    "4": "d"
  },
  "preserved_edges": [
    ["0,1", "a,c"],
    ["0,2", "a,b"],
    ["1,3", "c,e"],
    ["2,4", "b,d"],
    ["3,4", "e,d"]
  ]
}
```
