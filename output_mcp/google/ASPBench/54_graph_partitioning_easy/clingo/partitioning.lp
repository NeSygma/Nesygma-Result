% Vertices
vertex(0..7).

% Edges
edge(0,1). edge(0,4).
edge(1,2). edge(1,5).
edge(2,3). edge(2,6).
edge(3,7).
edge(4,5). edge(4,6).
edge(5,7).
edge(6,7).

% Partitioning
% Each vertex is in exactly one partition (1 or 2)
{ in_partition(V, 1) } :- vertex(V).
in_partition(V, 2) :- vertex(V), not in_partition(V, 1).

% Constraints: Exactly 4 vertices in each partition
:- #count { V : in_partition(V, 1) } != 4.
:- #count { V : in_partition(V, 2) } != 4.

% Crossing edges
% Since edge(U, V) is defined with U < V, crossing(U, V) will also have U < V.
crossing(U, V) :- edge(U, V), in_partition(U, P1), in_partition(V, P2), P1 != P2.

% Objective: Minimize cut size
cut_size(N) :- N = #count { U, V : crossing(U, V) }.
#minimize { N : cut_size(N) }.

% Output formatting
partition_1(V) :- in_partition(V, 1).
partition_2(V) :- in_partition(V, 2).
cut_edge(U, V) :- crossing(U, V).
balance(4, 4, "balanced").

#show partition_1/1.
#show partition_2/1.
#show cut_size/1.
#show cut_edge/2.
#show balance/3.