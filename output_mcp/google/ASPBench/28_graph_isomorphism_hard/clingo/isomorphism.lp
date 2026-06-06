% --- Domains ---
vertex1(1..8).
vertex2(a;b;c;d;e;f;g;h).

% --- Graph G1 Data ---
color(1, red). color(2, red). color(5, red). color(6, red).
color(3, blue). color(4, blue). color(7, blue). color(8, blue).
special(1).

edge1(1,3,10). edge1(1,4,20). edge1(2,3,20). edge1(2,4,10).
edge1(5,7,10). edge1(5,8,20). edge1(6,7,20). edge1(6,8,10).
edge1(1,5,30). edge1(2,6,30). edge1(3,7,40). edge1(4,8,40).

% --- Graph G2 Data ---
color(a, red). color(b, red). color(e, red). color(f, red).
color(c, blue). color(d, blue). color(g, blue). color(h, blue).
special(a).

edge2(a,c,10). edge2(a,d,20). edge2(b,c,20). edge2(b,d,10).
edge2(e,g,10). edge2(e,h,20). edge2(f,g,20). edge2(f,h,10).
edge2(a,e,30). edge2(b,f,30). edge2(c,g,40). edge2(d,h,40).

% --- Isomorphism Logic ---
% Bijection
{ map(U, V) : vertex2(V) } = 1 :- vertex1(U).
{ map(U, V) : vertex1(U) } = 1 :- vertex2(V).

% Color Preservation
:- map(U, V), color(U, C1), color(V, C2), C1 != C2.

% Special Vertex Preservation
:- map(U, V), special(U), not special(V).
:- map(U, V), not special(U), special(V).

% Edge and Weight Preservation
% Normalize edges for comparison
edge1_norm(U1, U2, W) :- edge1(U1, U2, W), U1 < U2.
edge1_norm(U2, U1, W) :- edge1(U1, U2, W), U2 < U1.
edge2_norm(V1, V2, W) :- edge2(V1, V2, W), V1 < V2.
edge2_norm(V2, V1, W) :- edge2(V1, V2, W), V2 < V1.

:- edge1_norm(U1, U2, W), map(U1, V1), map(U2, V2), not edge2_norm(V1, V2, W).
:- edge2_norm(V1, V2, W), map(U1, V1), map(U2, V2), not edge1_norm(U1, U2, W).

% Forbidden Subgraph: 3-cycle in G2 involving special vertex with weight 60
% A 3-cycle is (V1, V2), (V2, V3), (V3, V1)
% Weight = W1 + W2 + W3 = 60
% Special vertex is 'a'
is_triangle(V1, V2, V3, W1, W2, W3) :- 
    edge2_norm(V1, V2, W1), edge2_norm(V2, V3, W2), edge2_norm(V3, V1, W3),
    V1 < V2, V2 < V3.

has_special(V1, V2, V3) :- is_triangle(V1, V2, V3, _, _, _), special(V1).
has_special(V1, V2, V3) :- is_triangle(V1, V2, V3, _, _, _), special(V2).
has_special(V1, V2, V3) :- is_triangle(V1, V2, V3, _, _, _), special(V3).

:- is_triangle(V1, V2, V3, W1, W2, W3), 
   has_special(V1, V2, V3),
   W1 + W2 + W3 = 60.

% --- Output Mapping ---
is_isomorphic :- map(_, _).
option(true) :- is_isomorphic.
option(false) :- not is_isomorphic.

#show map/2.
#show is_isomorphic/0.