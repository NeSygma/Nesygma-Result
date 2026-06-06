% Define the vertices
vertex(0..15).

% Define partitions
partition(1..4).

% Assign each vertex to a partition (1-4)
1 { assign(V, P) : partition(P) } 1 :- vertex(V).

% Constraint: Each partition must have exactly 4 vertices
:- { assign(V, P) : vertex(V) } != 4, partition(P).

% Define edges with weights (undirected)
edge(0, 1, 10). edge(0, 2, 10). edge(0, 3, 10).
edge(1, 2, 10). edge(1, 3, 10). edge(2, 3, 10).
edge(4, 5, 10). edge(4, 6, 10). edge(4, 7, 10).
edge(5, 6, 10). edge(5, 7, 10). edge(6, 7, 10).
edge(8, 9, 10). edge(8, 10, 10). edge(8, 11, 10).
edge(9, 10, 10). edge(9, 11, 10). edge(10, 11, 10).
edge(12, 13, 10). edge(12, 14, 10). edge(12, 15, 10).
edge(13, 14, 10). edge(13, 15, 10). edge(14, 15, 10).
edge(3, 4, 1). edge(7, 8, 2). edge(11, 12, 3). edge(15, 0, 1).
edge(1, 6, 2). edge(5, 10, 3). edge(9, 14, 1).

% For undirected graph, check edges where endpoints are in different partitions
cross_edge(U, V, W) :- assign(U, P1), assign(V, P2), P1 != P2, edge(U, V, W).

% Calculate total cut weight
cut_weight(W) :- W = #sum { W1 : cross_edge(_, _, W1) }.

% Minimize the cut weight
#minimize { W : cut_weight(W) }.

% Show the solution
#show assign/2.
#show cut_weight/1.