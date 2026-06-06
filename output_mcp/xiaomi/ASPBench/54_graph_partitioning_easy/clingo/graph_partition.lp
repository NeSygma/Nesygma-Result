% ==============================
% Balanced Graph Partitioning
% Partition 8 vertices into two sets of 4
% Minimize edges crossing between partitions
% ==============================

% --- Domain ---
vertex(0..7).

% --- Edges (undirected, stored with V1 < V2) ---
edge(0,1).
edge(0,4).
edge(1,2).
edge(1,5).
edge(2,3).
edge(2,6).
edge(3,7).
edge(4,5).
edge(4,6).
edge(5,7).
edge(6,7).

% --- Partition assignment ---
% Each vertex must be in exactly one partition (1 or 2)
1 { in_partition(V, 1); in_partition(V, 2) } 1 :- vertex(V).

% --- Balance constraint ---
% Exactly 4 vertices in partition 1
:- #count { V : in_partition(V, 1) } != 4.

% Exactly 4 vertices in partition 2 (automatically satisfied if partition 1 has 4)
% But let's be explicit for clarity
:- #count { V : in_partition(V, 2) } != 4.

% --- Cut edges ---
% An edge crosses if its endpoints are in different partitions
cut_edge(V1, V2) :- edge(V1, V2), in_partition(V1, 1), in_partition(V2, 2).
cut_edge(V1, V2) :- edge(V1, V2), in_partition(V1, 2), in_partition(V2, 1).

% --- Cut size ---
cut_size(N) :- N = #count { V1, V2 : cut_edge(V1, V2) }.

% --- Optimization: minimize cut size ---
#minimize { N : cut_size(N) }.

% --- Output ---
#show in_partition/2.
#show cut_edge/2.
#show cut_size/1.