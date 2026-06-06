% Steiner Tree Problem
% Instance: vertices 0-6, terminals {0,5,6}

% --- Data ---
vertex(0..6).
terminal(0). terminal(5). terminal(6).

% Edges: edge(U, V, W)
edge(0,1,3). edge(0,2,5).
edge(1,3,2). edge(1,4,4).
edge(2,3,1). edge(2,5,6).
edge(3,4,3). edge(3,5,3). edge(3,6,2).
edge(4,5,2).
edge(5,6,4).

% Make edges undirected (symmetric)
edge(V, U, W) :- edge(U, V, W).

% --- Domain for tree edges ---
% Choose which edges are in the tree
{ tree_edge(U, V, W) } :- edge(U, V, W).

% --- Constraints ---

% 1. All terminals must be connected (reachable from terminal 0)
% First, define reachable from terminal 0
reachable(0).
reachable(V) :- reachable(U), tree_edge(U, V, _).
reachable(V) :- reachable(U), tree_edge(V, U, _).

% Every terminal must be reachable
:- terminal(T), not reachable(T).

% 2. Tree structure: no cycles
% A tree with N vertices has exactly N-1 edges
% Count vertices in the tree
in_tree(V) :- tree_edge(V, _, _).
in_tree(V) :- tree_edge(_, V, _).

% Count tree edges
tree_edge_count(N) :- N = #count { U, V, W : tree_edge(U, V, W), U < V }.

% Count vertices in tree
tree_vertex_count(N) :- N = #count { V : in_tree(V) }.

% Tree property: edges = vertices - 1
:- tree_edge_count(E), tree_vertex_count(V), E != V - 1.

% 3. Only valid edges from graph (already enforced by choice rule domain)

% 4. Edge weights match graph (already enforced by choice rule domain)

% --- Objective: Minimize total weight ---
#minimize { W, U, V : tree_edge(U, V, W), U < V }.

% --- Output ---
#show tree_edge/3.
#show total_weight/1.

total_weight(W) :- W = #sum { Wt, U, V : tree_edge(U, V, Wt), U < V }.