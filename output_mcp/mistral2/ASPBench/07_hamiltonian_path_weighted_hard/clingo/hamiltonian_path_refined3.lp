% Define the time steps (vertices in the path)
time(0..99).

% Define the vertices (0 to 99)
vertex(0..99).

% Start and end vertices
start(0).
end(99).

% Define edge weights and forbidden edges

% Chain edges (weight 1)
edge(I, I+1, 1) :- vertex(I), I < 99.

% Local swap gadgets every 4 vertices starting at 2 (weight 3)
edge(B, B+2, 3) :- N=0..23, B=2+4*N, B+2 <= 99.
edge(B+2, B+1, 3) :- N=0..23, B=2+4*N, B+1 <= 99.
edge(B+1, B+3, 3) :- N=0..23, B=2+4*N, B+3 <= 99.

% Skips of length 2 at multiples of 4 (weight 4)
edge(S, S+2, 4) :- N=0..24, S=4*N, S+2 <= 99.

% Jumps of length 3 for vertices ≡ 1 (mod 4) (weight 5)
edge(T, T+3, 5) :- N=0..23, T=1+4*N, T+3 <= 99.

% Long bridges of length 4 at multiples of 5 (weight 6)
edge(U, U+4, 6) :- K=0..19, U=5*K, U+4 <= 99.

% Forbidden edges
forbidden(0,2).
forbidden(1,3).

% Periodic forbids
forbidden(F, F+2) :- N=0..11, F=2+8*N, F+2 <= 99.
forbidden(G, G+2) :- N=0..12, G=8*N, G+2 <= 99.
forbidden(H, H+3) :- N=0..11, H=1+8*N, H+3 <= 99.
forbidden(L, L+4) :- M=0..9, L=10*M+5, L+4 <= 99.

% Path construction: path(T, V) means vertex V is at position T in the path
{ path(T, V) : vertex(V) } = 1 :- time(T).

% Ensure the path starts at 0 and ends at 99
:- start(V), path(0, V), V != 0.
:- end(V), path(99, V), V != 99.

% Ensure each vertex appears exactly once in the path
:- vertex(V), not { path(T, V) : time(T) } = 1.

% Ensure the path follows directed edges and avoids forbidden edges
:- path(T, V), path(T+1, W), not edge(V, W, _), V != W.
:- path(T, V), path(T+1, W), forbidden(V, W).

% Calculate the total cost
edge_cost(T, C) :- path(T, V), path(T+1, W), edge(V, W, C), time(T), T < 99.
total_cost(C) :- C = #sum{ C1 : edge_cost(_, C1) }.

% Minimize the total cost
#minimize{ C : total_cost(C) }.

% Show the path and cost
#show path/2.
#show total_cost/1.