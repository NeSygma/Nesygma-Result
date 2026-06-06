% Vertices
v1(0). v1(1). v1(2). v1(3). v1(4).
v2(a). v2(b). v2(c). v2(d). v2(e).

% Edges G1 (undirected)
edge1(0,1). edge1(1,0).
edge1(0,2). edge1(2,0).
edge1(1,3). edge1(3,1).
edge1(2,4). edge1(4,2).
edge1(3,4). edge1(4,3).

% Edges G2 (undirected)
edge2(a,b). edge2(b,a).
edge2(a,c). edge2(c,a).
edge2(b,d). edge2(d,b).
edge2(c,e). edge2(e,c).
edge2(d,e). edge2(e,d).

% Bijection: each v1 maps to exactly one v2
1 { mapping(U,V) : v2(V) } 1 :- v1(U).
% each v2 has exactly one preimage
1 { mapping(U,V) : v1(U) } 1 :- v2(V).

% Adjacency preservation
:- edge1(U,V), mapping(U,FU), mapping(V,FV), not edge2(FU,FV).

% Reverse adjacency preservation
:- edge2(U,V), mapping(U1,U), mapping(V1,V), not edge1(U1,V1).

% Degree calculation
degree1(U,N) :- v1(U), N = #count{V : edge1(U,V)}.
degree2(V,N) :- v2(V), N = #count{W : edge2(V,W)}.

% Degree preservation
:- mapping(U,V), degree1(U,N1), degree2(V,N2), N1 != N2.

% Preserved edges
preserved_edge(U,V,FU,FV) :- edge1(U,V), mapping(U,FU), mapping(V,FV), edge2(FU,FV).

% is_isomorphic
is_isomorphic :- mapping(U,V).

#show mapping/2.
#show is_isomorphic.
#show preserved_edge/4.