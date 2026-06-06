% Vertices
vertex(1..7).

% Edges (undirected, stored as edge(X,Y) with X < Y)
edge(1,2).
edge(1,3).
edge(2,3).
edge(2,4).
edge(3,5).
edge(4,6).
edge(5,6).
edge(5,7).
edge(6,7).

% Adjacency (symmetric)
adj(X,Y) :- edge(X,Y).
adj(Y,X) :- edge(X,Y).

% Choice: select vertices for the dominating set
{ in_ds(V) } :- vertex(V).

% Constraint: every vertex must be dominated
% A vertex is dominated if it's in the set OR adjacent to a vertex in the set
dominated(V) :- in_ds(V).
dominated(V) :- adj(V, U), in_ds(U).

:- vertex(V), not dominated(V).

% Count the size
ds_size(N) :- N = #count{V : in_ds(V)}.

% Minimize the size
#minimize { 1,V : in_ds(V) }.

% Output
#show in_ds/1.
#show ds_size/1.