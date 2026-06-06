% Graph Isomorphism with Forbidden Subgraph Constraints

% ===== Domain Definitions =====
% G1 vertices
vertex1(1). vertex1(2). vertex1(3). vertex1(4).
vertex1(5). vertex1(6). vertex1(7). vertex1(8).

% G2 vertices
vertex2(a). vertex2(b). vertex2(c). vertex2(d).
vertex2(e). vertex2(f). vertex2(g). vertex2(h).

% Colors
color1(1, red). color1(2, red). color1(5, red). color1(6, red).
color1(3, blue). color1(4, blue). color1(7, blue). color1(8, blue).

color2(a, red). color2(b, red). color2(e, red). color2(f, red).
color2(c, blue). color2(d, blue). color2(g, blue). color2(h, blue).

% Special vertices
special1(1).
special2(a).

% Edges in G1 (undirected, stored with U < V)
edge1(1,3,10). edge1(1,4,20). edge1(2,3,20). edge1(2,4,10).
edge1(5,7,10). edge1(5,8,20). edge1(6,7,20). edge1(6,8,10).
edge1(1,5,30). edge1(2,6,30). edge1(3,7,40). edge1(4,8,40).

% Edges in G2 (undirected, stored with U < V)
edge2(a,c,10). edge2(a,d,20). edge2(b,c,20). edge2(b,d,10).
edge2(e,g,10). edge2(e,h,20). edge2(f,g,20). edge2(f,h,10).
edge2(a,e,30). edge2(b,f,30). edge2(c,g,40). edge2(d,h,40).

% ===== Mapping Generation =====
% Each G1 vertex maps to exactly one G2 vertex
{ map(V1, V2) : vertex2(V2) } 1 :- vertex1(V1).

% Each G2 vertex is mapped from exactly one G1 vertex
{ map(V1, V2) : vertex1(V1) } 1 :- vertex2(V2).

% ===== Constraints =====
% Color preservation
:- color1(V1, C), map(V1, V2), not color2(V2, C).

% Special vertex preservation
:- special1(V1), map(V1, V2), not special2(V2).
:- special2(V2), map(V1, V2), not special1(V1).

% Edge and weight preservation (both directions)
:- edge1(U1, V1, W), map(U1, U2), map(V1, V2), not edge2(U2, V2, W).
:- edge2(U2, V2, W), map(U1, U2), map(V1, V2), not edge1(U1, V1, W).

% Forbidden triangle constraint:
% No triangle in G2 with total weight 60 that involves a special vertex.
% We write three separate constraints for each possible special vertex in the triangle.
:- map(U1, X), map(V1, Y), map(W1, Z),
   U1 != V1, V1 != W1, U1 != W1,
   edge2(X,Y,Wxy), edge2(X,Z,Wxz), edge2(Y,Z,Wyz),
   Wxy + Wxz + Wyz = 60,
   special1(U1).

:- map(U1, X), map(V1, Y), map(W1, Z),
   U1 != V1, V1 != W1, U1 != W1,
   edge2(X,Y,Wxy), edge2(X,Z,Wxz), edge2(Y,Z,Wyz),
   Wxy + Wxz + Wyz = 60,
   special1(V1).

:- map(U1, X), map(V1, Y), map(W1, Z),
   U1 != V1, V1 != W1, U1 != W1,
   edge2(X,Y,Wxy), edge2(X,Z,Wxz), edge2(Y,Z,Wyz),
   Wxy + Wxz + Wyz = 60,
   special1(W1).

% ===== Output Definitions =====
% Isomorphism exists if there is at least one mapping that satisfies all constraints.
% Since constraints are hard, if the program is satisfiable, then is_isomorphic is true.
is_isomorphic :- map(_, _).

% Mapping output (only if isomorphic)
mapping(V1, V2) :- map(V1, V2), is_isomorphic.

% Preserved weighted edges (normalized: sorted vertices in G2)
preserved_edge(U1, V1, W, U2, V2) :-
   edge1(U1, V1, W),
   map(U1, U2), map(V1, V2),
   U2 < V2,
   is_isomorphic.
preserved_edge(U1, V1, W, V2, U2) :-
   edge1(U1, V1, W),
   map(U1, U2), map(V1, V2),
   V2 < U2,
   is_isomorphic.

% ===== Show Directives =====
#show is_isomorphic/0.
#show mapping/2.
#show preserved_edge/5.