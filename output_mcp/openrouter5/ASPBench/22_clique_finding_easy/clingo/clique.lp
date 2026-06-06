% Vertices
vertex(0..6).

% Edges (undirected - symmetric)
edge(0,1). edge(0,2). edge(0,3).
edge(1,2). edge(1,3). edge(1,4).
edge(2,3). edge(2,5).
edge(3,4). edge(3,5).
edge(4,5). edge(4,6).
edge(5,6).

% Make edges symmetric
edge(X,Y) :- edge(Y,X), vertex(X), vertex(Y).

% No self-loops
:- edge(X,X).

% Choose which vertices are in the clique
{ in_clique(V) : vertex(V) }.

% Constraint: every pair of vertices in the clique must be connected by an edge
:- in_clique(U), in_clique(V), U < V, not edge(U,V).

% Maximize the clique size
#maximize { 1,V : in_clique(V) }.

% Show results
#show in_clique/1.
#show clique_size/1.
clique_size(N) :- N = #count { V : in_clique(V) }.