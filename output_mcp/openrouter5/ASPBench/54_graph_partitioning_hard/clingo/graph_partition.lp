% Graph Partitioning Problem
% 16 vertices into 4 equal-sized partitions (4 vertices each)
% Minimize total weight of edges crossing between partitions

% Domain: vertices
vertex(0..15).

% Domain: partitions
partition(1..4).

% Edges with weights
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

% Inter-cluster edges
edge(3,4,1). edge(7,8,2). edge(11,12,3). edge(15,0,1).
edge(1,6,2). edge(5,10,3). edge(9,14,1).

% Symmetric edges (undirected) - derive reverse direction
edge(V2,V1,W) :- edge(V1,V2,W).

% Each vertex assigned to exactly one partition
1 { assign(V,P) : partition(P) } 1 :- vertex(V).

% Each partition has exactly 4 vertices
:- partition(P), not #count { V : assign(V,P) } = 4.

% Define crossing edges: edge (V1,V2) crosses if V1 and V2 are in different partitions
crossing(V1,V2,W) :- edge(V1,V2,W), assign(V1,P1), assign(V2,P2), P1 != P2.

% Total cut weight
cut_weight(W) :- W = #sum { Wgt, V1, V2 : crossing(V1,V2,Wgt) }.

% Since edges are undirected and we have both directions, divide by 2
% Actually, we should only count each undirected edge once.
% Let's fix: only count when V1 < V2
crossing_undirected(V1,V2,W) :- edge(V1,V2,W), V1 < V2, assign(V1,P1), assign(V2,P2), P1 != P2.
cut_weight_undirected(W) :- W = #sum { Wgt, V1, V2 : crossing_undirected(V1,V2,Wgt) }.

% Minimize the cut weight
#minimize { Wgt, V1, V2 : crossing_undirected(V1,V2,Wgt) }.

% Show results
#show assign/2.
#show cut_weight_undirected/1.
#show crossing_undirected/3.