% Hamiltonian Path in Directed Weighted Graph
% Vertices 0..99, start 0, end 99

% Domain definitions
vertex(0..99).
position(0..99).

% Forbidden edges
forbidden(0,2).
forbidden(1,3).

% Periodic forbids
forbidden(F, F+2) :- N = 0..11, F = 2 + 8*N.
forbidden(G, G+2) :- N = 0..12, G = 8*N, G+2 <= 99.
forbidden(H, H+3) :- N = 0..11, H = 1 + 8*N.
forbidden(L, L+4) :- M = 0..9, L = 10*M + 5, L+4 <= 99.

% Allowed edges from categories (excluding forbidden)
% Chain edges
edge_from_categories(i, i+1, 1) :- i = 0..98.

% Local swap gadgets
edge_from_categories(B, B+2, 3) :- N = 0..23, B = 2 + 4*N.
edge_from_categories(B+2, B+1, 3) :- N = 0..23, B = 2 + 4*N.
edge_from_categories(B+1, B+3, 3) :- N = 0..23, B = 2 + 4*N.

% Skips of length 2
edge_from_categories(S, S+2, 4) :- N = 0..24, S = 4*N, S+2 <= 99.

% Jumps of length 3
edge_from_categories(T, T+3, 5) :- N = 0..23, T = 1 + 4*N.

% Long bridges of length 4
edge_from_categories(U, U+4, 6) :- K = 0..19, U = 5*K.

% Allowed edges are those from categories that are not forbidden
allowed_edge(U,V,W) :- edge_from_categories(U,V,W), not forbidden(U,V).

% Path representation: pos(V,P) means vertex V is at position P
% Each vertex appears exactly once
1 { pos(V, P) : position(P) } 1 :- vertex(V).
% Each position has exactly one vertex
1 { pos(V, P) : vertex(V) } 1 :- position(P).

% Start and end fixed
pos(0,0).
pos(99,99).

% Successor relation
next(V,U) :- pos(V,P), pos(U,P+1), P = 0..98.

% Constrain that next edge must be allowed
:- next(V,U), not allowed_edge(V,U,W).

% Edge used with weight
edge_used(V,U,W) :- next(V,U), allowed_edge(V,U,W).

% Total cost
cost(S) :- S = #sum { W,V,U : edge_used(V,U,W) }.

% Minimize total cost
#minimize { C : cost(C) }.

% Output
#show path_at/2.
path_at(P,V) :- pos(V,P).

#show min_cost/1.
min_cost(C) :- cost(C).

#show exists/0.
exists.

% Also show cost for debugging
#show cost/1.