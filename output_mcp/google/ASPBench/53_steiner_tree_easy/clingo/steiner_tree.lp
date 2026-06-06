% --- Data ---
vertex(0..6).
terminal(0; 5; 6).

edge(0, 1, 3).
edge(0, 2, 5).
edge(1, 3, 2).
edge(1, 4, 4).
edge(2, 3, 1).
edge(2, 5, 6).
edge(3, 4, 3).
edge(3, 5, 3).
edge(3, 6, 2).
edge(4, 5, 2).
edge(5, 6, 4).

% Undirected edges
edge(V, U, W) :- edge(U, V, W).

% --- Choice Rule ---
% Select edges to be in the tree
{ in_tree(U, V, W) } :- edge(U, V, W), U < V.

% Symmetry
in_tree(V, U, W) :- in_tree(U, V, W).

% --- Tree Properties ---
% Vertices in the tree
in_tree_vertex(V) :- in_tree(U, V, W).

% All terminals must be in the tree
:- terminal(T), not in_tree_vertex(T).

% Connectivity
connected(U, V) :- in_tree(U, V, W).
reachable(U, V) :- connected(U, V).
reachable(U, W) :- reachable(U, V), connected(V, W).

% All terminals must be connected to each other
:- terminal(T1), terminal(T2), T1 < T2, not reachable(T1, T2).

% Tree structure: E = V - 1
num_edges(E) :- E = #count { U, V : in_tree(U, V, W), U < V }.
num_vertices(V) :- V = #count { X : in_tree_vertex(X) }.
:- num_edges(E), num_vertices(V), E != V - 1.

% --- Objective ---
total_weight(W) :- W = #sum { Weight, U, V : in_tree(U, V, Weight), U < V }.
#minimize { W : total_weight(W) }.

% --- Output ---
#show in_tree/3.
#show total_weight/1.
#show in_tree_vertex/1.