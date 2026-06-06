% Vertices of G1
vertex1(0). vertex1(1). vertex1(2). vertex1(3). vertex1(4).
% Vertices of G2
vertex2(a). vertex2(b). vertex2(c). vertex2(d). vertex2(e).
% Index for ordering G2 vertices
idx2(a,0). idx2(b,1). idx2(c,2). idx2(d,3). idx2(e,4).
% Edges of G1 (undirected, both directions)
edge1(0,1). edge1(1,0).
edge1(0,2). edge1(2,0).
edge1(1,3). edge1(3,1).
edge1(2,4). edge1(4,2).
edge1(3,4). edge1(4,3).
% Edges of G2 (undirected)
edge2(a,b). edge2(b,a).
edge2(a,c). edge2(c,a).
edge2(b,d). edge2(d,b).
edge2(c,e). edge2(e,c).
edge2(d,e). edge2(e,d).
% Bijection: each vertex of G1 maps to exactly one vertex of G2
1 { map(U,V) : vertex2(V) } 1 :- vertex1(U).
% Injectivity: no two G1 vertices map to same G2 vertex
:- map(U,V), map(W,V), U != W.
% Inverse mapping helper
invmap(V,U) :- map(U,V).
% Degree computation
deg1(U,N) :- vertex1(U), N = #count { V : edge1(U,V) }.
deg2(V,N) :- vertex2(V), N = #count { W : edge2(V,W) }.
% Degree preservation
:- map(U,V), deg1(U,D1), deg2(V,D2), D1 != D2.
% Adjacency preservation (G1 -> G2)
:- edge1(U,V), map(U,FU), map(V,FV), not edge2(FU,FV).
% Reverse adjacency preservation (G2 -> G1)
:- edge2(X,Y), invmap(X,U), invmap(Y,V), not edge1(U,V).
% Define isomorphic when a bijection satisfying constraints exists
isomorphic :- map(_, _).
% Preserve edges for output
preserved(U,V) :- edge1(U,V), map(U,FU), map(V,FV), edge2(FU,FV).
% Lexicographically minimal mapping (unique solution)
#minimize { Idx@1 : map(0,V), idx2(V,Idx) }.
#minimize { Idx@2 : map(1,V), idx2(V,Idx) }.
#minimize { Idx@3 : map(2,V), idx2(V,Idx) }.
#minimize { Idx@4 : map(3,V), idx2(V,Idx) }.
#minimize { Idx@5 : map(4,V), idx2(V,Idx) }.
#show isomorphic/0.
#show map/2.
#show preserved/2.