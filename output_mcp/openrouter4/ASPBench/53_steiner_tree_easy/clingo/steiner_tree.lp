% --- Graph Data ---
vertex(0..6).

% Edges with weights (undirected, canonical ordering U < V)
edge(0,1,3). edge(0,2,5).
edge(1,3,2). edge(1,4,4).
edge(2,3,1). edge(2,5,6).
edge(3,4,3). edge(3,5,3). edge(3,6,2).
edge(4,5,2).
edge(5,6,4).

% Terminals
terminal(0;5;6).

% --- Choice: which edges to select? ---
{ selected(U,V,W) : edge(U,V,W) }.

% Symmetric version for easy traversal
selected_sym(U,V,W) :- selected(U,V,W).
selected_sym(V,U,W) :- selected(U,V,W).

% --- Connectivity from root terminal (0) ---
reachable(0).
reachable(V) :- selected_sym(U,V,W), reachable(U).

% All terminals must be reachable
:- terminal(V), not reachable(V).

% All selected edges must be incident to reachable vertices
:- selected(U,V,W), not reachable(U).
:- selected(U,V,W), not reachable(V).

% Vertices actually in the tree
vertex_in_tree(V) :- reachable(V), vertex(V).

% --- Tree condition: |E| = |V| - 1 ---
edge_count(E) :- E = #count { U,V,W : selected(U,V,W) }.
vertex_count(N) :- N = #count { V : vertex_in_tree(V) }.
:- edge_count(E), vertex_count(N), E != N - 1.

% --- Minimize total weight ---
#minimize { W,U,V : selected(U,V,W) }.

% --- Output predicates ---
total_weight(TW) :- TW = #sum { W,U,V : selected(U,V,W) }.

steiner_vertex(V) :- vertex_in_tree(V), not terminal(V).

connected_component(1).

tree_edge(U,V,W) :- selected(U,V,W).

% Show output
#show total_weight/1.
#show tree_edge/3.
#show steiner_vertex/1.
#show terminal/1.
#show connected_component/1.