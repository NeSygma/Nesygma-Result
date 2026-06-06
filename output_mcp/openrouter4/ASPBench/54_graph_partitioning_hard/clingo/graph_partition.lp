%% Graph Partitioning: 16 vertices into 4 equal-sized sets
%% Minimize crossing edges weight

%% Domains
vertex(0..15).
partition(1..4).

%% Edges (undirected, given with u < v)
edge(0,1,10). edge(0,2,10). edge(0,3,10).
edge(1,2,10). edge(1,3,10).
edge(2,3,10).

edge(4,5,10). edge(4,6,10). edge(4,7,10).
edge(5,6,10). edge(5,7,10).
edge(6,7,10).

edge(8,9,10). edge(8,10,10). edge(8,11,10).
edge(9,10,10). edge(9,11,10).
edge(10,11,10).

edge(12,13,10). edge(12,14,10). edge(12,15,10).
edge(13,14,10). edge(13,15,10).
edge(14,15,10).

%% Inter-cluster edges
edge(3,4,1). edge(7,8,2). edge(11,12,3). edge(15,0,1).
edge(1,6,2). edge(5,10,3). edge(9,14,1).

%% Assignment: each vertex to exactly one partition
{ assign(V, P) : partition(P) } = 1 :- vertex(V).

%% Balance constraint: exactly 4 vertices per partition
:- partition(P), #count { V : assign(V, P) } != 4.

%% Crossing edges: endpoints in different partitions
crossing(V1, V2, W) :- edge(V1, V2, W), assign(V1, P1), assign(V2, P2), P1 != P2.

%% Minimize total cut weight
#minimize { W, V1, V2 : crossing(V1, V2, W) }.

%% Output
cut_weight(W) :- W = #sum { Wt, V1, V2 : crossing(V1, V2, Wt) }.
#show assign/2.
#show cut_weight/1.