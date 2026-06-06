% Graph 1 (G1) facts
vertex1(0). vertex1(1). vertex1(2). vertex1(3). vertex1(4).

edge1(0, 1). edge1(0, 2).
edge1(1, 3).
edge1(2, 4).
edge1(3, 4).

% Graph 2 (G2) facts
vertex2(a). vertex2(b). vertex2(c). vertex2(d). vertex2(e).

edge2(a, b). edge2(a, c).
edge2(b, d).
edge2(c, e).
edge2(d, e).

% Compute degrees for G1
degree1(V, D) :- 
    vertex1(V), 
    D = #count { U : edge1(V, U) }.

% Compute degrees for G2
degree2(V, D) :- 
    vertex2(V), 
    D = #count { U : edge2(V, U) }.

% Ensure the number of vertices match (necessary for isomorphism)
:- #count { V : vertex1(V) } != #count { V : vertex2(V) }.

% Ensure the number of edges match (necessary for isomorphism)
:- #count { U,V : edge1(U, V) } != #count { U,V : edge2(U, V) }.

% Choice rule for bijection: each vertex in G1 maps to exactly one vertex in G2
{ mapping(V1, V2) : vertex2(V2) } = 1 :- vertex1(V1).

% Ensure the mapping is injective (one-to-one)
:- mapping(V1, V2), mapping(V1p, V2), V1 != V1p.

% Ensure the mapping is surjective (onto) by checking all vertices in G2 are mapped to
:- vertex2(V2), not mapping(V1, V2) : vertex1(V1).

% Adjacency preservation: for every edge (u,v) in G1, (f(u),f(v)) must be an edge in G2
preserved_edge(U, V, U2, V2) :-
    edge1(U, V),
    mapping(U, U2),
    mapping(V, V2),
    edge2(U2, V2).

% Ensure all edges in G1 are preserved
:- edge1(U, V), not preserved_edge(U, V, _, _).

% Degree preservation: degree of u in G1 must equal degree of f(u) in G2
degree_preserved(V1, V2) :-
    mapping(V1, V2),
    degree1(V1, D),
    degree2(V2, D).

:- vertex1(V1), vertex2(V2), mapping(V1, V2), not degree_preserved(V1, V2).

% If all constraints are satisfied, the graphs are isomorphic
is_isomorphic :- preserved_edge(_, _, _, _), degree_preserved(_, _).

% Sentinel atom to indicate a solution exists
solution_exists :- is_isomorphic.

% Output atoms
#show mapping/2.
#show is_isomorphic/0.
#show preserved_edge/4.
#show solution_exists/0.