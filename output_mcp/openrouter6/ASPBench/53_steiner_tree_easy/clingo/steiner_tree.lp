% Steiner Tree Problem
% Vertices 0..6, terminals 0,5,6

% Vertices
vertex(0..6).

% Terminal vertices
terminal(0).
terminal(5).
terminal(6).

% Edges (undirected, stored with U < V)
edge(0,1,3).
edge(0,2,5).
edge(1,3,2).
edge(1,4,4).
edge(2,3,1).
edge(2,5,6).
edge(3,4,3).
edge(3,5,3).
edge(3,6,2).
edge(4,5,2).
edge(5,6,4).

% Symmetric edge predicate for convenience
sym_edge(U,V,W) :- edge(U,V,W).
sym_edge(V,U,W) :- edge(U,V,W).

% Choice rule: select edges (only one direction, U < V)
{ selected_edge(U,V) } :- edge(U,V,W).

% Symmetric selected edge for reachability
selected_sym(U,V) :- selected_edge(U,V).
selected_sym(V,U) :- selected_edge(U,V).

% Included vertices: terminals or incident to selected edges
included(V) :- terminal(V).
included(V) :- selected_sym(U,V).

% Root (choose terminal 0 as root)
root(0).

% Reachability from root via selected edges
reachable(V) :- root(V).
reachable(V) :- reachable(U), selected_sym(U,V).

% Connectivity: all included vertices must be reachable from root
:- included(V), not reachable(V).

% Count selected edges and included vertices
num_selected_edges(N) :- N = #count{U,V : selected_edge(U,V)}.
num_included_vertices(M) :- M = #count{V : included(V)}.

% Tree property: number of selected edges = number of included vertices - 1
:- num_selected_edges(N), num_included_vertices(M), N != M - 1.

% Total weight of selected edges
total_weight(S) :- S = #sum{W,U,V : selected_edge(U,V), edge(U,V,W)}.

% Minimize total weight
#minimize { S : total_weight(S) }.

% Steiner vertices (non-terminals included)
steiner_vertex(V) :- included(V), not terminal(V).

% Show relevant information
#show vertex/1.
#show terminal/1.
#show selected_edge/2.
#show included/1.
#show steiner_vertex/1.
#show total_weight/1.
#show root/1.
#show reachable/1.