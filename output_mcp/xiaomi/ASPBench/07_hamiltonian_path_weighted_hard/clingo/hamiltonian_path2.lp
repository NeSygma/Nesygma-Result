% Vertices
vertex(0..99).

% Start and end
start(0).
end(99).

% ============ EDGE GENERATION ============

% 1. Chain edges (weight 1): edge(i, i+1) for i in 0..98
edge(I, I+1, 1) :- I = 0..98.

% 2. Local swap gadgets every 4 vertices starting at 2 (weight 3)
% For N in 0..23, B = 2 + 4*N
edge(B, B+2, 3) :- B = 2+4*N, N = 0..23, B+3 <= 99.
edge(B+2, B+1, 3) :- B = 2+4*N, N = 0..23, B+3 <= 99.
edge(B+1, B+3, 3) :- B = 2+4*N, N = 0..23, B+3 <= 99.

% 3. Skips of length 2 at multiples of 4 (weight 4)
edge(S, S+2, 4) :- S = 4*N, N = 0..24, S+2 <= 99.

% 4. Jumps of length 3 for vertices ≡ 1 (mod 4) (weight 5)
edge(T, T+3, 5) :- T = 1+4*N, N = 0..23, T+3 <= 99.

% 5. Long bridges of length 4 at multiples of 5 (weight 6)
edge(U, U+4, 6) :- U = 5*K, K = 0..19, U+4 <= 99.

% ============ FORBIDDEN EDGES ============

% Base forbids
forbidden(0, 2).
forbidden(1, 3).

% Periodic forbids: F = 2 + 8*N, forbid (F, F+2)
forbidden(F, F+2) :- F = 2+8*N, N = 0..11, F+2 <= 99.

% Periodic forbids: G = 8*N, forbid (G, G+2)
forbidden(G, G+2) :- G = 8*N, N = 0..12, G+2 <= 99.

% Periodic forbids: H = 1 + 8*N, forbid (H, H+3)
forbidden(H, H+3) :- H = 1+8*N, N = 0..11, H+3 <= 99.

% Periodic forbids: L = 10*M + 5, forbid (L, L+4)
forbidden(L, L+4) :- L = 10*M+5, M = 0..9, L+4 <= 99.

% ============ VALID EDGES ============

% An edge is valid if it exists and is not forbidden
valid_edge(X, Y, W) :- edge(X, Y, W), not forbidden(X, Y).

% ============ HAMILTONIAN PATH ============

% For each vertex, choose which position it occupies
1 { at_pos(V, P) : pos(P) } 1 :- vertex(V).

% For each position, exactly one vertex
1 { at_pos(V, P) : vertex(V) } 1 :- pos(P).

% Positions
pos(0..99).

% Start and end constraints
at_pos(0, 0).
at_pos(99, 99).

% Consecutive positions must be connected by a valid edge
:- pos(P), P < 99, at_pos(V1, P), at_pos(V2, P+1), not valid_edge(V1, V2, _).

% ============ COST CALCULATION ============

% The edge used at position P
used_edge(V1, V2, W, P) :- pos(P), P < 99, at_pos(V1, P), at_pos(V2, P+1), valid_edge(V1, V2, W).

% Total cost
total_cost(C) :- C = #sum { W, P : used_edge(_, _, W, P) }.

% ============ OPTIMIZATION ============

#minimize { C : total_cost(C) }.

% ============ OUTPUT ============

#show at_pos/2.
#show total_cost/1.