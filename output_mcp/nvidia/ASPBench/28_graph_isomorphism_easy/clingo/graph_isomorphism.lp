vertex1(0). vertex1(1). vertex1(2). vertex1(3). vertex1(4).
vertex2(a). vertex2(b). vertex2(c). vertex2(d). vertex2(e).

edge1(0,1). edge1(1,0).
edge1(0,2). edge1(2,0).
edge1(1,3). edge1(3,1).
edge1(2,4). edge1(4,2).
edge1(3,4). edge1(4,3).

edge2(a,b). edge2(b,a).
edge2(a,c). edge2(c,a).
edge2(b,d). edge2(d,b).
edge2(c,e). edge2(e,c).
edge2(d,e). edge2(e,d).

% Bijection mapping
1 { mapping(V1, V2) : vertex2(V2) } 1 :- vertex1(V1).
1 { mapping(V1, V2) : vertex1(V1) } 1 :- vertex2(V2).

% Adjacency preservation (forward direction)
:- mapping(U, FU), mapping(V, FV), edge1(U, V), not edge2(FU, FV).

% Isomorphism flag
isomorphic :- mapping(0, _).

% Preserved edge correspondence
preserved_edge(U, V, FU, FV) :- mapping(U, FU), mapping(V, FV), edge1(U, V).

% Output
#show mapping/2.
#show preserved_edge/4.
#show isomorphic.