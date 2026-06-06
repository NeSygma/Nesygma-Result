% Graph partitioning problem: 16 vertices, 4 partitions of size 4, minimize cut weight.

% Vertices
vertex(0..15).

% Partitions
partition(1..4).

% Edges (undirected, store each edge once with u < v)
% Cluster 1 (0-3)
edge(0,1,10). edge(0,2,10). edge(0,3,10).
edge(1,2,10). edge(1,3,10).
edge(2,3,10).

% Cluster 2 (4-7)
edge(4,5,10). edge(4,6,10). edge(4,7,10).
edge(5,6,10). edge(5,7,10).
edge(6,7,10).

% Cluster 3 (8-11)
edge(8,9,10). edge(8,10,10). edge(8,11,10).
edge(9,10,10). edge(9,11,10).
edge(10,11,10).

% Cluster 4 (12-15)
edge(12,13,10). edge(12,14,10). edge(12,15,10).
edge(13,14,10). edge(13,15,10).
edge(14,15,10).

% Inter-cluster edges
edge(3,4,1). edge(7,8,2). edge(11,12,3). edge(15,0,1).
edge(1,6,2). edge(5,10,3). edge(9,14,1).

% Ensure each vertex assigned to exactly one partition
1 { assigned(V, P) : partition(P) } 1 :- vertex(V).

% Ensure each partition has exactly 4 vertices
4 { assigned(V, P) : vertex(V) } 4 :- partition(P).

% Define cut edges: edges whose endpoints are in different partitions
cut_edge(U, V, W) :- edge(U, V, W), assigned(U, P1), assigned(V, P2), P1 != P2.

% Compute total cut weight
cut_weight(S) :- S = #sum { W, U, V : cut_edge(U, V, W) }.

% Minimize cut weight
#minimize { W@1 : cut_edge(_, _, W) }.

% Output partition assignments
#show assigned/2.

% Output cut edges
#show cut_edge/3.

% Output cut weight
#show cut_weight/1.

% Also show partition sizes for verification
partition_size(P, N) :- partition(P), N = #count { V : assigned(V, P) }.
#show partition_size/2.