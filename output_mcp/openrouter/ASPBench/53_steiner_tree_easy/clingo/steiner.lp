% Vertices
v(0..6).

% Terminals
terminal(0).
terminal(5).
terminal(6).

% Edges with weights (undirected, store only one direction)
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

% Choice of edges in the Steiner tree
{ sel(U,V) : edge(U,V,_) }.

% Selected vertices are those incident to selected edges or terminals
selV(X) :- sel(X,_).
selV(Y) :- sel(_,Y).
selV(T) :- terminal(T).

% Reachability from a root terminal (choose 0 as root)
reachable(0).
reachable(Y) :- reachable(X), sel(X,Y).
reachable(Y) :- reachable(X), sel(Y,X).

% Connectivity: all selected vertices must be reachable
:- selV(X), not reachable(X).

% Acyclicity: number of edges = number of vertices - 1
edges_cnt(E) :- E = #count{U,V : sel(U,V)}.
verts_cnt(V) :- V = #count{X : selV(X)}.
:- edges_cnt(E), verts_cnt(V), E != V - 1.

% Total weight of selected edges
total_weight(T) :- T = #sum{W,U,V : sel(U,V), edge(U,V,W)}.

% Steiner vertices (selected non-terminals)
steiner(X) :- selV(X), not terminal(X).

% Optimization: minimize total weight
#minimize { W,U,V : sel(U,V), edge(U,V,W) }.

% Show results
#show sel/2.
#show total_weight/1.
#show steiner/1.
#show terminal/1.