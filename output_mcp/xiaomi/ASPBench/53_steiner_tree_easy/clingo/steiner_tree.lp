% Steiner Tree Problem - Minimum weight tree connecting all terminals

% ============ DOMAIN ============
% Vertices
vertex(0..6).

% Terminals
terminal(0).
terminal(5).
terminal(6).

% Edges with weights (undirected, store both directions)
edge(0,1,3). edge(1,0,3).
edge(0,2,5). edge(2,0,5).
edge(1,3,2). edge(3,1,2).
edge(1,4,4). edge(4,1,4).
edge(2,3,1). edge(3,2,1).
edge(2,5,6). edge(5,2,6).
edge(3,4,3). edge(4,3,3).
edge(3,5,3). edge(5,3,3).
edge(3,6,2). edge(6,3,2).
edge(4,5,2). edge(5,4,2).
edge(5,6,4). edge(6,5,4).

% ============ CHOICE RULES ============
% Select edges to include in the tree
{ select(U,V) : edge(U,V,_) }.

% ============ CONSTRAINTS ============

% 1. All terminals must be in the tree (connected)
% A vertex is in the tree if it's an endpoint of a selected edge
in_tree(V) :- select(V,_).
in_tree(V) :- select(_,V).

% Every terminal must be in the tree
:- terminal(V), not in_tree(V).

% 2. Tree connectivity: exactly one connected component
% Use reachability from vertex 0 (arbitrary root)
reachable(0) :- in_tree(0).
reachable(V) :- reachable(U), select(U,V).
reachable(V) :- reachable(U), select(V,U).

% All vertices in the tree must be reachable from 0
:- in_tree(V), not reachable(V).

% 3. No cycles: For a tree with n vertices, there must be exactly n-1 edges
% Count vertices in tree
tree_size(N) :- N = #count{V : in_tree(V)}.

% Count edges in tree (each edge counted once: U < V)
tree_edge_count(M) :- M = #count{U,V : select(U,V), U < V}.

% Tree property: edges = vertices - 1
:- tree_size(N), tree_edge_count(M), M != N - 1.

% 4. Only use valid edges (already enforced by select domain)

% ============ OBJECTIVE ============
% Calculate total weight
total_weight(W) :- W = #sum{Wt,U,V : select(U,V), edge(U,V,Wt), U < V}.

% Minimize total weight
#minimize { W : total_weight(W) }.

% ============ OUTPUT ============
#show select/2.
#show total_weight/1.
#show in_tree/1.