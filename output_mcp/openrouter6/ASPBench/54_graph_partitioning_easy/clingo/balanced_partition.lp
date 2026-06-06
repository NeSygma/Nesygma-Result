% Balanced Graph Partitioning Problem
% Vertices: 0,1,2,3,4,5,6,7
% Edges: as given

% --- Domain ---
vertex(0..7).

% --- Edges (undirected, store with ordering U < V) ---
edge(0,1). edge(0,4).
edge(1,2). edge(1,5).
edge(2,3). edge(2,6).
edge(3,7).
edge(4,5). edge(4,6).
edge(5,7).
edge(6,7).

% --- Partition assignment ---
% Each vertex assigned to exactly one partition (1 or 2)
1 { partition(V, 1); partition(V, 2) } 1 :- vertex(V).

% --- Exactly 4 vertices in each partition ---
:- #count{ V : partition(V, 1) } != 4.
:- #count{ V : partition(V, 2) } != 4.

% --- Crossing edges ---
% Edge (U,V) crosses if vertices are in different partitions
cross(U,V) :- edge(U,V), partition(U,1), partition(V,2).
cross(U,V) :- edge(U,V), partition(U,2), partition(V,1).

% --- Cut size (number of crossing edges) ---
cut_size(N) :- N = #count{ U,V : cross(U,V) }.

% --- Minimize cut size ---
#minimize { 1, U,V : cross(U,V) }.

% --- Output atoms for required format ---
% Partition 1 list
partition_1(V) :- partition(V, 1).
% Partition 2 list
partition_2(V) :- partition(V, 2).
% Cut edges (from < to)
cut_edge(U,V) :- cross(U,V), U < V.
% Balance status
balance_ok :- #count{ V : partition(V,1) } = 4, #count{ V : partition(V,2) } = 4.

% --- Show directives ---
#show partition_1/1.
#show partition_2/1.
#show cut_size/1.
#show cut_edge/2.
#show balance_ok/0.