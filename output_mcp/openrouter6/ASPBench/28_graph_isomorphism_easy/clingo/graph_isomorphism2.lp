% Graph Isomorphism Problem

% Define vertices of G1
vertex1(0). vertex1(1). vertex1(2). vertex1(3). vertex1(4).

% Define vertices of G2 (strings)
vertex2("a"). vertex2("b"). vertex2("c"). vertex2("d"). vertex2("e").

% Define edges of G1 (undirected, stored with X < Y to avoid duplication)
edge1(0,1). edge1(0,2). edge1(1,3). edge1(2,4). edge1(3,4).

% Define edges of G2 (undirected, stored with X < Y lexicographically)
edge2("a","b"). edge2("a","c"). edge2("b","d"). edge2("c","e"). edge2("d","e").

% Mapping: each vertex1 maps to exactly one vertex2
1 { mapping(X,Y) : vertex2(Y) } 1 :- vertex1(X).

% Bijection: each vertex2 maps to exactly one vertex1
1 { mapping(X,Y) : vertex1(X) } 1 :- vertex2(Y).

% Adjacency preservation: for every edge in G1, the mapped edge exists in G2
% Since edges are undirected, we need to consider both orders for mapping
:- edge1(X,Y), mapping(X,U), mapping(Y,V), not edge2(U,V), not edge2(V,U).

% Reverse preservation: for every edge in G2, there must be a corresponding edge in G1
edge1_mapped(U,V) :- edge1(X,Y), mapping(X,U), mapping(Y,V).
edge1_mapped(U,V) :- edge1(X,Y), mapping(X,V), mapping(Y,U).
:- edge2(U,V), not edge1_mapped(U,V).

% Degree preservation: degree of vertex in G1 equals degree of its image in G2
% Compute degree of each vertex in G1 (count edges incident to it)
deg1(X, N) :- vertex1(X), N = #count{Y : edge1(X,Y), vertex1(Y)}.
% Compute degree of each vertex in G2
deg2(Y, N) :- vertex2(Y), N = #count{Z : edge2(Y,Z), vertex2(Z)}.
% Constraint: degrees must match under mapping
:- vertex1(X), mapping(X,Y), deg1(X, D1), deg2(Y, D2), D1 != D2.

% Derive is_isomorphic if a mapping exists (all constraints satisfied)
is_isomorphic :- mapping(_,_).

% Output mapping only if is_isomorphic holds
mapping_output(X,Y) :- mapping(X,Y), is_isomorphic.

% Output preserved edges: for each edge1, output the corresponding edge2
preserved_edge(edge1(X,Y), edge2(U,V)) :- edge1(X,Y), mapping(X,U), mapping(Y,V), is_isomorphic.
preserved_edge(edge1(X,Y), edge2(V,U)) :- edge1(X,Y), mapping(X,V), mapping(Y,U), is_isomorphic.

% If not isomorphic, output a flag
is_not_isomorphic :- not is_isomorphic.

% Show directives
#show is_isomorphic/0.
#show is_not_isomorphic/0.
#show mapping_output/2.
#show preserved_edge/2.