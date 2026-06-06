% Vertices
vertex(0..99).

% Start and end
start(0).
end(99).

% ============ EDGE GENERATION ============

% 1. Chain edges (weight 1): edge(i, i+1) for i in 0..98
edge(I, I+1, 1) :- I = 0..98.

% 2. Local swap gadgets every 4 vertices starting at 2 (weight 3)
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

% Periodic forbids
forbidden(F, F+2) :- F = 2+8*N, N = 0..11, F+2 <= 99.
forbidden(G, G+2) :- G = 8*N, N = 0..12, G+2 <= 99.
forbidden(H, H+3) :- H = 1+8*N, N = 0..11, H+3 <= 99.
forbidden(L, L+4) :- L = 10*M+5, M = 0..9, L+4 <= 99.

% ============ VALID EDGES ============

valid_edge(X, Y, W) :- edge(X, Y, W), not forbidden(X, Y).

% ============ SUCCESSOR-BASED HAMILTONIAN PATH ============

% For each vertex (except end), choose exactly one successor
1 { next(V, U) : valid_edge(V, U, _) } 1 :- vertex(V), not end(V).

% End vertex has no successor
{ next(99, U) } 0 :- vertex(U).

% For each vertex (except start), choose exactly one predecessor
1 { prev(U, V) : valid_edge(U, V, _) } 1 :- vertex(V), not start(V).

% Start vertex has no predecessor
{ prev(U, 0) } 0 :- vertex(U).

% next and prev must be consistent
prev(U, V) :- next(U, V).

% ============ CYCLE PREVENTION ============

% Reachability from start
reachable(0).
reachable(V) :- reachable(U), next(U, V).

% All vertices must be reachable
:- vertex(V), not reachable(V).

% ============ COST CALCULATION ============

% Cost of each edge used
edge_cost(V, U, W) :- next(V, U), valid_edge(V, U, W).

% Total cost
total_cost(C) :- C = #sum { W, V, U : edge_cost(V, U, W) }.

% ============ OPTIMIZATION ============

#minimize { C : total_cost(C) }.

% ============ OUTPUT ============

#show next/2.
#show total_cost/1.