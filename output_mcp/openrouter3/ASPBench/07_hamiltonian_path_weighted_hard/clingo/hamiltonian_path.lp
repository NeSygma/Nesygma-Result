% Hamiltonian Path with Minimum Cost in Directed Graph

% Domain declaration
vertex(0..99).

% 1. Chain edges (weight 1): For all i in 0..98: edge (i, i+1) with weight 1
edge(I, I+1, 1) :- vertex(I), I < 99.

% 2. Local swap gadgets every 4 vertices starting at 2 (weight 3)
% For N in 0..23, let B = 2 + 4*N:
%   Edge (B, B+2) with weight 3
%   Edge (B+2, B+1) with weight 3
%   Edge (B+1, B+3) with weight 3
edge(B, B+2, 3) :- N = 0..23, B = 2 + 4*N, vertex(B), vertex(B+2).
edge(B+2, B+1, 3) :- N = 0..23, B = 2 + 4*N, vertex(B+2), vertex(B+1).
edge(B+1, B+3, 3) :- N = 0..23, B = 2 + 4*N, vertex(B+1), vertex(B+3).

% 3. Skips of length 2 at multiples of 4 (weight 4)
% For N in 0..24, let S = 4*N with S+2 <= 99:
edge(S, S+2, 4) :- N = 0..24, S = 4*N, S+2 <= 99, vertex(S), vertex(S+2).

% 4. Jumps of length 3 for vertices ≡ 1 (mod 4) (weight 5)
% For N in 0..23, let T = 1 + 4*N:
edge(T, T+3, 5) :- N = 0..23, T = 1 + 4*N, vertex(T), vertex(T+3).

% 5. Long bridges of length 4 at multiples of 5 (weight 6)
% For K in 0..19, let U = 5*K:
edge(U, U+4, 6) :- K = 0..19, U = 5*K, vertex(U), vertex(U+4).

% Forbidden edges
forbidden(0, 2).
forbidden(1, 3).

% Periodic forbids
forbidden(F, F+2) :- N = 0..11, F = 2 + 8*N, vertex(F), vertex(F+2).
forbidden(G, G+2) :- N = 0..12, G = 8*N, G+2 <= 99, vertex(G), vertex(G+2).
forbidden(H, H+3) :- N = 0..11, H = 1 + 8*N, vertex(H), vertex(H+3).
forbidden(L, L+4) :- M = 0..9, L = 10*M + 5, L+4 <= 99, vertex(L), vertex(L+4).

% Choice rule: select exactly one outgoing edge for each vertex (except end vertex)
% We'll use position-based approach instead
% Each vertex appears exactly once in the path
1 { path_vertex(V, P) : vertex(V) } 1 :- P = 0..99.
1 { path_vertex(V, P) : P = 0..99 } 1 :- vertex(V).

% Path starts at 0 and ends at 99
path_vertex(0, 0).
path_vertex(99, 99).

% Consecutive vertices must be connected by an edge
edge_used(U, V) :- path_vertex(U, P), path_vertex(V, P+1), edge(U, V, _).

% No forbidden edges used
:- edge_used(U, V), forbidden(U, V).

% Calculate total cost
total_cost(C) :- C = #sum { W, U, V : edge_used(U, V), edge(U, V, W) }.

% Minimize cost
#minimize { C : total_cost(C) }.

% Show results
#show vertex/1.
#show edge/3.
#show path_vertex/2.
#show edge_used/2.
#show total_cost/1.