% Define vertices
vertex(1..8).

% Define edges (undirected)
edge(1,2). edge(1,3). edge(1,4).
edge(2,5).
edge(3,6). edge(3,7).
edge(4,8).
edge(5,6).
edge(6,7).
edge(7,8).

% Make edges symmetric (undirected)
edge(X,Y) :- edge(Y,X), vertex(X), vertex(Y).

% Choose which vertices are in the independent set
{ in_set(V) } :- vertex(V).

% Constraint: No two vertices in the set can be connected by an edge
:- in_set(V1), in_set(V2), edge(V1,V2), V1 < V2.

% Maximize the number of vertices in the independent set
#maximize { 1,V : in_set(V) }.

#show in_set/1.
#show size/1.
size(N) :- N = #count { V : in_set(V) }.