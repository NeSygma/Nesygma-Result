% Graph 1 (G1)
g1_vertex(0;1;2;3;4).
g1_edge(0,1). g1_edge(1,0).
g1_edge(0,2). g1_edge(2,0).
g1_edge(1,3). g1_edge(3,1).
g1_edge(2,4). g1_edge(4,2).
g1_edge(3,4). g1_edge(4,3).

% Graph 2 (G2)
g2_vertex(a;b;c;d;e).
g2_edge(a,b). g2_edge(b,a).
g2_edge(a,c). g2_edge(c,a).
g2_edge(b,d). g2_edge(d,b).
g2_edge(c,e). g2_edge(e,c).
g2_edge(d,e). g2_edge(e,d).

% Bijection: each G1 vertex maps to exactly one G2 vertex
1 { map(V1, V2) : g2_vertex(V2) } 1 :- g1_vertex(V1).

% Each G2 vertex is mapped by exactly one G1 vertex
:- g2_vertex(V2), not 1 { map(V1, V2) : g1_vertex(V1) } 1.

% Forward: adjacency preservation
% For every edge (u,v) in G1, (f(u), f(v)) must be an edge in G2
:- g1_edge(U, V), map(U, U2), map(V, V2), not g2_edge(U2, V2).

% Reverse: every G2 edge corresponds to a G1 edge
:- g2_edge(U2, V2), map(U, U2), map(V, V2), not g1_edge(U, V).

% is_isomorphic is true (satisfiable = isomorphic)
is_isomorphic.

% Mapping output: G1 vertex -> G2 vertex
mapping(V1, V2) :- map(V1, V2).

% Preserved edges (undirected, show each once with V1 < V2)
% Format: preserved_edge("V1,V2", "f(V1),f(V2)")
preserved_edge(V1, V2, U2, V2_out) :- g1_edge(V1, V2), V1 < V2, map(V1, U2), map(V2, V2_out).

#show is_isomorphic/0.
#show mapping/2.
#show preserved_edge/4.