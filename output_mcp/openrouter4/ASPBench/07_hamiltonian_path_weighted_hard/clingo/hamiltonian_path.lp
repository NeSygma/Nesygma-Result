% Define vertices
vertex(0..99).

% 1. Chain edges (weight 1)
edge(I, I+1, 1) :- I = 0..98.

% 2. Local swap gadgets every 4 vertices starting at 2 (weight 3)
edge(B, B+2, 3) :- N = 0..23, B = 2 + 4*N, B+2 <= 99.
edge(B+2, B+1, 3) :- N = 0..23, B = 2 + 4*N, B+2 <= 99, B+1 <= 99.
edge(B+1, B+3, 3) :- N = 0..23, B = 2 + 4*N, B+1 <= 99, B+3 <= 99.

% 3. Skips of length 2 at multiples of 4 (weight 4)
edge(S, S+2, 4) :- N = 0..24, S = 4*N, S+2 <= 99.

% 4. Jumps of length 3 for vertices ≡ 1 mod 4 (weight 5)
edge(T, T+3, 5) :- N = 0..23, T = 1 + 4*N, T+3 <= 99.

% 5. Long bridges of length 4 at multiples of 5 (weight 6)
edge(U, U+4, 6) :- K = 0..19, U = 5*K, U+4 <= 99.

% Forbidden edges
forbidden(0,2).
forbidden(1,3).
forbidden(F, F+2) :- N = 0..11, F = 2 + 8*N.
forbidden(G, G+2) :- N = 0..12, G = 8*N, G+2 <= 99.
forbidden(H, H+3) :- N = 0..11, H = 1 + 8*N.
forbidden(L, L+4) :- M = 0..9, L = 10*M + 5, L+4 <= 99.

% Available edges (not forbidden)
available(X, Y, W) :- edge(X, Y, W), not forbidden(X, Y).

% Choose successor edges
{succ(X, Y)} :- available(X, Y, _).

% Each non-end vertex has exactly one outgoing edge
:- vertex(X), X != 99, #count{Y : succ(X, Y)} != 1.

% End vertex (99) has no outgoing edges
:- succ(99, _).

% Each non-start vertex has exactly one incoming edge
:- vertex(Y), Y != 0, #count{X : succ(X, Y)} != 1.

% Start vertex (0) has no incoming edges
:- succ(_, 0).

% Reachability from start (ensures a single path, no cycles)
reaches(0).
reaches(Y) :- reaches(X), succ(X, Y).
:- vertex(V), not reaches(V).

% Compute total cost
total_cost(C) :- C = #sum{W, X, Y : succ(X, Y), available(X, Y, W)}.

% Output the path as a sequence of positions
path_pos(0, 0).
path_pos(P+1, Y) :- path_pos(P, X), succ(X, Y), P < 99.

% Minimize total cost
#minimize { W, X, Y : succ(X, Y), available(X, Y, W) }.

#show path_pos/2.
#show total_cost/1.