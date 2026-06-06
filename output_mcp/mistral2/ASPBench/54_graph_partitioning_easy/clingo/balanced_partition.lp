% Define the vertices and edges
vertex(0..7).
edge(0,1). edge(0,4).
edge(1,2). edge(1,5).
edge(2,3). edge(2,6).
edge(3,7).
edge(4,5). edge(4,6).
edge(5,7).
edge(6,7).

% Assign each vertex to either partition 1 or partition 2
% Use a choice rule to allow Clingo to explore all possible assignments
{ in_partition(V, 1) : vertex(V) } 1 :- vertex(V).
{ in_partition(V, 2) : vertex(V) } 1 :- vertex(V).

% Ensure each vertex is assigned to exactly one partition
:- vertex(V), in_partition(V, 1), in_partition(V, 2).
:- vertex(V), not in_partition(V, 1), not in_partition(V, 2).

% Ensure exactly 4 vertices in partition 1 and 4 in partition 2
:- { in_partition(V, 1) : vertex(V) } != 4.
:- { in_partition(V, 2) : vertex(V) } != 4.

% Define a crossing edge: an edge (u,v) where u and v are in different partitions
crossing_edge(U, V) :-
    edge(U, V),
    in_partition(U, P1),
    in_partition(V, P2),
    P1 != P2,
    U < V.  % Ensure each edge is only counted once (from < to)

% Count the number of crossing edges (cut size)
cut_size(N) :- N = #count{ U, V : crossing_edge(U, V) }.

% Define the partitions for output
partition_1(V) :- in_partition(V, 1).
partition_2(V) :- in_partition(V, 2).

% Define the cut edges for output (with from and to fields)
cut_edge(from(U), to(V)) :- crossing_edge(U, V).

% Define balance status
balance_status(balanced) :-
    { in_partition(V, 1) : vertex(V) } = 4,
    { in_partition(V, 2) : vertex(V) } = 4.
balance_status(unbalanced) :- not balance_status(balanced).

% Show the required outputs
#show partition_1/1.
#show partition_2/1.
#show cut_size/1.
#show cut_edge/2.
#show balance_status/1.