% Balanced Graph Partitioning Problem

% Domain: Vertices
vertex(0). vertex(1). vertex(2). vertex(3).
vertex(4). vertex(5). vertex(6). vertex(7).

% Edges (undirected, stored as both directions for convenience)
edge(0,1). edge(1,0).
edge(0,4). edge(4,0).
edge(1,2). edge(2,1).
edge(1,5). edge(5,1).
edge(2,3). edge(3,2).
edge(2,6). edge(6,2).
edge(3,7). edge(7,3).
edge(4,5). edge(5,4).
edge(4,6). edge(6,4).
edge(5,7). edge(7,5).
edge(6,7). edge(7,6).

% Partitions: 1 or 2
partition(1). partition(2).

% Choice rule: Each vertex assigned to exactly one partition
1 { in_partition(V, P) : partition(P) } 1 :- vertex(V).

% Constraint: Exactly 4 vertices in each partition
:- #count{ V : in_partition(V, 1) } != 4.
:- #count{ V : in_partition(V, 2) } != 4.

% Identify crossing edges (edges where endpoints are in different partitions)
cut_edge(U, V) :- edge(U, V), U < V, in_partition(U, P1), in_partition(V, P2), P1 != P2.

% Calculate cut size
cut_size(N) :- N = #count{ U, V : cut_edge(U, V) }.

% Partition sizes (for output)
partition_size(1, N1) :- N1 = #count{ V : in_partition(V, 1) }.
partition_size(2, N2) :- N2 = #count{ V : in_partition(V, 2) }.

% Output predicates for solution
partition_1(V) :- in_partition(V, 1).
partition_2(V) :- in_partition(V, 2).

% Balance status
balance("balanced") :- partition_size(1, 4), partition_size(2, 4).

% Minimize cut size
#minimize { 1, U, V : cut_edge(U, V) }.

% Show relevant output
#show partition_1/1.
#show partition_2/1.
#show cut_size/1.
#show cut_edge/2.
#show balance/0.