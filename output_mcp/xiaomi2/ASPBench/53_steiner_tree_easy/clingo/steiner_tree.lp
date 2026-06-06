% ==============================
% Steiner Tree Problem in ASP
% ==============================

% --- Domain: Vertices ---
vertex(0..6).

% --- Domain: Edges (undirected, stored in both directions) ---
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

% --- Terminal vertices (must all be in the tree) ---
terminal(0). terminal(5). terminal(6).

% --- Decision: Which vertices are in the Steiner tree ---
% All terminals are mandatory
in_tree(V) :- terminal(V).
% Non-terminals are optional (Steiner vertices)
{ in_tree(V) } :- vertex(V), not terminal(V).

% --- Decision: Which edges are selected for the tree ---
% Only edges between two vertices that are both in the tree
% Store canonical form V1 < V2 to avoid duplicates
{ tree_edge(V1, V2) } :- edge(V1, V2, _), in_tree(V1), in_tree(V2), V1 < V2.

% --- Constraint 1: Tree structure ---
% A tree on N vertices has exactly N-1 edges
num_vertices(N) :- N = #count{ V : in_tree(V) }.
num_edges(E)    :- E = #count{ V1,V2 : tree_edge(V1,V2) }.
:- num_vertices(N), num_edges(E), E != N - 1.

% --- Constraint 2: Connectivity ---
% Define reachability from root vertex 0 (a terminal, always in tree)
reachable(0) :- in_tree(0).
reachable(V2) :- reachable(V1), tree_edge(V1, V2).
reachable(V2) :- reachable(V1), tree_edge(V2, V1).

% Every vertex in the tree must be reachable from the root
:- in_tree(V), not reachable(V).

% --- Objective: Minimize total weight ---
#minimize { W, V1, V2 : tree_edge(V1, V2), edge(V1, V2, W) }.

% --- Derived output predicates ---
total_weight(W) :- W = #sum { Wt,V1,V2 : tree_edge(V1,V2), edge(V1,V2,Wt) }.
steiner_vertex(V) :- in_tree(V), not terminal(V).

% --- Display ---
#show tree_edge/2.
#show in_tree/1.
#show steiner_vertex/1.
#show total_weight/1.