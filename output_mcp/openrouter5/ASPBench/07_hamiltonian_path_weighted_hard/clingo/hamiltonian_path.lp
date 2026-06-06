% Domain: vertices 0..99
vertex(0..99).

% Start and end
start(0).
end(99).

% Time steps: we need exactly 100 vertices in path, so 99 edges
time(0..99).

% --- Edge definitions ---

% 1. Chain edges (weight 1): (i, i+1) for i in 0..98
edge(I, I+1, 1) :- I = 0..98.

% 2. Local swap gadgets every 4 vertices starting at 2 (weight 3)
% For N in 0..23, B = 2 + 4*N
edge(B, B+2, 3) :- N = 0..23, B = 2 + 4*N, B+2 <= 99.
edge(B+2, B+1, 3) :- N = 0..23, B = 2 + 4*N, B+1 <= 99.
edge(B+1, B+3, 3) :- N = 0..23, B = 2 + 4*N, B+3 <= 99.

% 3. Skips of length 2 at multiples of 4 (weight 4)
% For N in 0..24, S = 4*N with S+2 <= 99
edge(S, S+2, 4) :- N = 0..24, S = 4*N, S+2 <= 99.

% 4. Jumps of length 3 for vertices ≡ 1 (mod 4) (weight 5)
% For N in 0..23, T = 1 + 4*N
edge(T, T+3, 5) :- N = 0..23, T = 1 + 4*N, T+3 <= 99.

% 5. Long bridges of length 4 at multiples of 5 (weight 6)
% For K in 0..19, U = 5*K
edge(U, U+4, 6) :- K = 0..19, U = 5*K, U+4 <= 99.

% --- Forbidden edges ---
% Base forbids
forbidden(0,2).
forbidden(1,3).

% Periodic forbids
% For N in 0..11, F = 2 + 8*N: forbid (F, F+2)
forbidden(F, F+2) :- N = 0..11, F = 2 + 8*N, F+2 <= 99.
% For N in 0..12, G = 8*N with G+2 <= 99: forbid (G, G+2)
forbidden(G, G+2) :- N = 0..12, G = 8*N, G+2 <= 99.
% For N in 0..11, H = 1 + 8*N: forbid (H, H+3)
forbidden(H, H+3) :- N = 0..11, H = 1 + 8*N, H+3 <= 99.
% For M in 0..9, L = 10*M + 5 with L+4 <= 99: forbid (L, L+4)
forbidden(L, L+4) :- M = 0..9, L = 10*M + 5, L+4 <= 99.

% Available edges: edges that are not forbidden
avail_edge(U, V, W) :- edge(U, V, W), not forbidden(U, V).

% --- Hamiltonian path modeling using successor relation ---

% Each vertex (except 99) has exactly one successor
{ succ(V, U) : avail_edge(V, U, _) } 1 :- vertex(V), V != 99.

% Each vertex (except 0) has exactly one predecessor
{ pred(V, U) : avail_edge(U, V, _) } 1 :- vertex(V), V != 0.

% succ and pred are consistent
succ(V, U) :- pred(U, V).
pred(U, V) :- succ(V, U).

% No vertex can be its own successor (no self-loops)
:- succ(V, V).

% No cycles: use reachability from start
% reachable(V) :- V = 0.
% reachable(U) :- reachable(V), succ(V, U).
% :- vertex(V), V != 0, not reachable(V).

% Alternative: use path ordering constraint
% Assign each vertex a position in the path
{ pos(V, P) : time(P) } 1 :- vertex(V).
:- vertex(V), not { pos(V, P) : time(P) } 1.
:- time(P), not { pos(V, P) : vertex(V) } 1.

% Start at position 0, end at position 99
pos(0, 0).
pos(99, 99).

% If succ(V, U) then pos(U) = pos(V) + 1
:- succ(V, U), pos(V, P1), pos(U, P2), P2 != P1 + 1.

% --- Cost calculation ---
cost_used(V, U, W) :- succ(V, U), avail_edge(V, U, W).

total_cost(C) :- C = #sum { W, V, U : cost_used(V, U, W) }.

% --- Optimization: minimize total cost ---
#minimize { C : total_cost(C) }.

% --- Output ---
% Show the path: vertex at each position
#show pos/2.
% Show total cost
#show total_cost/1.