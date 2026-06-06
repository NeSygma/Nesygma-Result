% Define the vertices
vertex(0..7).

% Define the edges (store each edge once with canonical ordering)
edge(0,1). edge(0,4).
edge(1,2). edge(1,5).
edge(2,3). edge(2,6).
edge(3,7).
edge(4,5). edge(4,6).
edge(5,7).
edge(6,7).

% Assign each vertex to a partition (1 or 2)
1 { in_partition(V, 1) ; in_partition(V, 2) } 1 :- vertex(V).

% Exactly 4 vertices in partition 1
:- { in_partition(V, 1) } != 4.

% Exactly 4 vertices in partition 2
:- { in_partition(V, 2) } != 4.

% Define crossing edges (canonical form: from < to)
crosses(E1, E2) :- edge(E1, E2), E1 < E2, in_partition(E1, P1), in_partition(E2, P2), P1 != P2.

% Count the number of crossing edges
cut_size(C) :- C = #count { E1, E2 : crosses(E1, E2) }.

% Minimize the cut size
#minimize { C : cut_size(C) }.

% Helper predicates for output
partition_1(V) :- in_partition(V, 1).
partition_2(V) :- in_partition(V, 2).

% Show the required output
#show partition_1/1.
#show partition_2/1.
#show cut_size/1.