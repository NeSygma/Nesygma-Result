% ===== DOMAIN: Graph G1 vertices =====
v1(1). v1(2). v1(3). v1(4). v1(5). v1(6). v1(7). v1(8).

% ===== DOMAIN: Graph G2 vertices =====
v2(a). v2(b). v2(c). v2(d). v2(e). v2(f). v2(g). v2(h).

% ===== COLORS =====
% G1 colors
color1(1, red). color1(2, red). color1(5, red). color1(6, red).
color1(3, blue). color1(4, blue). color1(7, blue). color1(8, blue).

% G2 colors
color2(a, red). color2(b, red). color2(e, red). color2(f, red).
color2(c, blue). color2(d, blue). color2(g, blue). color2(h, blue).

% ===== SPECIAL VERTICES =====
special1(1).
special2(a).

% ===== EDGES (normalized: smaller vertex first) =====
% G1 edges
edge1(1,3,10). edge1(1,4,20). edge1(2,3,20). edge1(2,4,10).
edge1(5,7,10). edge1(5,8,20). edge1(6,7,20). edge1(6,8,10).
edge1(1,5,30). edge1(2,6,30). edge1(3,7,40). edge1(4,8,40).

% G2 edges
edge2(a,c,10). edge2(a,d,20). edge2(b,c,20). edge2(b,d,10).
edge2(e,g,10). edge2(e,h,20). edge2(f,g,20). edge2(f,h,10).
edge2(a,e,30). edge2(b,f,30). edge2(c,g,40). edge2(d,h,40).

% ===== HELPER: undirected edge access (both directions) =====
has_edge1(U, V, W) :- edge1(U, V, W).
has_edge1(V, U, W) :- edge1(U, V, W).

has_edge2(U, V, W) :- edge2(U, V, W).
has_edge2(V, U, W) :- edge2(U, V, W).

% ===== CONSTRAINT 1: BIJECTION =====
% Each G1 vertex maps to exactly one G2 vertex
1 { map(V1, V2) : v2(V2) } 1 :- v1(V1).

% Each G2 vertex is the image of exactly one G1 vertex
1 { map(V1, V2) : v1(V1) } 1 :- v2(V2).

% ===== CONSTRAINT 2: COLOR PRESERVATION =====
% If V1 maps to V2, they must have the same color
:- map(V1, V2), color1(V1, C), not color2(V2, C).
:- map(V1, V2), color2(V2, C), not color1(V1, C).

% ===== CONSTRAINT 3: SPECIAL VERTEX PRESERVATION =====
:- map(V1, V2), special1(V1), not special2(V2).
:- map(V1, V2), special2(V2), not special1(V1).

% ===== CONSTRAINT 4: EDGE AND WEIGHT PRESERVATION =====
% Forward: edge in G1 => corresponding edge in G2 with same weight
:- map(U1, U2), map(V1, V2), has_edge1(U1, V1, W), not has_edge2(U2, V2, W).

% Backward: edge in G2 => corresponding edge in G1 with same weight
:- map(U1, U2), map(V1, V2), has_edge2(U2, V2, W), not has_edge1(U1, V1, W).

% ===== CONSTRAINT 5: FORBIDDEN SUBGRAPH (3-cycle with special vertex, weight=60) =====
% Detect all triangles in G2 (using normalized edges to avoid double-counting)
triangle(U, V, W) :- edge2(U, V, _), edge2(V, W, _), edge2(U, W, _), U < V, V < W.

% Triangle involves a special vertex in G2
triangle_with_special(U, V, W) :- triangle(U, V, W), special2(U).
triangle_with_special(U, V, W) :- triangle(U, V, W), special2(V).
triangle_with_special(U, V, W) :- triangle(U, V, W), special2(W).

% Compute total weight of triangle
tri_weight(U, V, W, S) :- triangle(U, V, W),
    edge2(U, V, W1), edge2(V, W, W2), edge2(U, W, W3),
    S = W1 + W2 + W3.

% Forbid any triangle with special vertex and total weight exactly 60
:- triangle_with_special(U, V, W), tri_weight(U, V, W, 60).

% ===== DERIVED OUTPUT =====
% Mark that a valid isomorphism was found
is_isomorphic :- map(_, _).

% Record preserved weighted edges (normalized: U1 < V1, U2 < V2)
preserved_edge(U1, V1, U2, V2, W) :- map(U1, U2), map(V1, V2), edge1(U1, V1, W), edge2(U2, V2, W).

% ===== SHOW DIRECTIVES =====
#show is_isomorphic.
#show map/2.
#show preserved_edge/5.