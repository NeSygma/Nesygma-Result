% Graph G1
vertex1(1..8).
red1(1). red1(2). red1(5). red1(6).
blue1(3). blue1(4). blue1(7). blue1(8).
special1(1).

edge1(1,3,10). edge1(1,4,20). edge1(2,3,20). edge1(2,4,10).
edge1(5,7,10). edge1(5,8,20). edge1(6,7,20). edge1(6,8,10).
edge1(1,5,30). edge1(2,6,30). edge1(3,7,40). edge1(4,8,40).

% Graph G2
vertex2(a;b;c;d;e;f;g;h).
red2(a). red2(b). red2(e). red2(f).
blue2(c). blue2(d). blue2(g). blue2(h).
special2(a).

edge2(a,c,10). edge2(a,d,20). edge2(b,c,20). edge2(b,d,10).
edge2(e,g,10). edge2(e,h,20). edge2(f,g,20). edge2(f,h,10).
edge2(a,e,30). edge2(b,f,30). edge2(c,g,40). edge2(d,h,40).

% Normalize edges (store with u < v)
edge1_norm(U,V,W) :- edge1(U,V,W), U < V.
edge1_norm(V,U,W) :- edge1(U,V,W), U > V.

edge2_norm(U,V,W) :- edge2(U,V,W), U < V.
edge2_norm(V,U,W) :- edge2(U,V,W), U > V.

% Mapping choice: bijection from G1 vertices to G2 vertices
1 { mapping(V1, V2) : vertex2(V2) } 1 :- vertex1(V1).
1 { mapping(V1, V2) : vertex1(V1) } 1 :- vertex2(V2).

% Color preservation
:- mapping(V1, V2), red1(V1), not red2(V2).
:- mapping(V1, V2), blue1(V1), not blue2(V2).

% Special vertex preservation
:- mapping(V1, V2), special1(V1), not special2(V2).
:- mapping(V1, V2), special2(V2), not special1(V1).

% Edge and weight preservation
preserved_edge(U1,V1,U2,V2,W) :-
    mapping(U1, U2),
    mapping(V1, V2),
    edge1_norm(U1,V1,W),
    edge2_norm(U2,V2,W).

:- edge1_norm(U1,V1,W), not preserved_edge(U1,V1,_,_,W).
:- preserved_edge(U1,V1,U2,V2,W), not edge2_norm(U2,V2,W).

% Forbidden subgraph: no 3-cycle involving special vertex with total weight 60
% A triangle is: special vertex S connected to A and B, and A connected to B
:- special2(S),
   mapping(S_G1, S),
   edge2_norm(S, A, W1),
   edge2_norm(S, B, W2),
   edge2_norm(A, B, W3),
   A != B,
   W1 + W2 + W3 = 60.

% Determine if isomorphic
is_isomorphic :- mapping(_, _).

% Output
#show is_isomorphic/0.
#show mapping/2.
#show preserved_edge/5.