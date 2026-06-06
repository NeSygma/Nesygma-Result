% Vertices
vertex(0..99).

% Edges
edge(I, I+1, 1) :- I = 0..98.
edge(B, B+2, 3) :- N = 0..23, B = 2 + 4*N.
edge(B+2, B+1, 3) :- N = 0..23, B = 2 + 4*N.
edge(B+1, B+3, 3) :- N = 0..23, B = 4*N + 5. % B+1 = 2+4N+1 = 3+4N. B+3 = 2+4N+3 = 5+4N.
% Wait, let's re-calculate the B+1, B+3 edge carefully.
% B = 2 + 4*N. B+1 = 3 + 4*N. B+3 = 5 + 4*N.
% Edge (B+1, B+3) is (3+4N, 5+4N).
edge(3+4*N, 5+4*N, 3) :- N = 0..23.

% Re-check edge definitions
% 1. Chain: (i, i+1) weight 1
% 2. Swap: B=2+4N. (B, B+2), (B+2, B+1), (B+1, B+3) weight 3
% 3. Skips: S=4N. (S, S+2) weight 4
% 4. Jumps: T=1+4N. (T, T+3) weight 5
% 5. Bridges: U=5K. (U, U+4) weight 6

% Let's rewrite edges clearly
edge(I, I+1, 1) :- I = 0..98.
edge(2+4*N, 4+4*N, 3) :- N = 0..23.
edge(4+4*N, 3+4*N, 3) :- N = 0..23.
edge(3+4*N, 5+4*N, 3) :- N = 0..23.
edge(4*N, 4*N+2, 4) :- N = 0..24, 4*N+2 <= 99.
edge(1+4*N, 4+4*N, 5) :- N = 0..23.
edge(5*K, 5*K+4, 6) :- K = 0..19, 5*K+4 <= 99.

% Forbidden edges
forbidden(0, 2).
forbidden(1, 3).
forbidden(2+8*N, 4+8*N) :- N = 0..11.
forbidden(8*N, 8*N+2) :- N = 0..12, 8*N+2 <= 99.
forbidden(1+8*N, 4+8*N) :- N = 0..11.
forbidden(10*M+5, 10*M+9) :- M = 0..9, 10*M+9 <= 99.

% Valid edges
valid_edge(U, V, W) :- edge(U, V, W), not forbidden(U, V).

% Hamiltonian path construction
% Use a successor relation to build the path
{ next(U, V) } :- valid_edge(U, V, _).

% Each vertex except 99 has exactly one successor
1 { next(U, V) : valid_edge(U, V, _) } 1 :- vertex(U), U != 99.
% Each vertex except 0 has exactly one predecessor
1 { next(U, V) : valid_edge(U, V, _) } 1 :- vertex(V), V != 0.

% Connectivity: Ensure all vertices are reachable from 0
reached(0).
reached(V) :- reached(U), next(U, V).
:- vertex(V), not reached(V).

% Cost calculation
total_cost(C) :- C = #sum { W, U, V : next(U, V), valid_edge(U, V, W) }.

% Objective: Minimize total cost
#minimize { C : total_cost(C) }.

% Output
#show next/2.
#show total_cost/1.