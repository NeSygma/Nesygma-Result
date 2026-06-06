% Vertices
vertex(1..8).

% Edges
edge(1,2). edge(1,3). edge(1,4).
edge(2,5).
edge(3,6). edge(3,7).
edge(4,8).
edge(5,6).
edge(6,7).
edge(7,8).

% Make edges undirected
edge(V, U) :- edge(U, V).

% Decision: Select vertices for the independent set
{ in_set(V) } :- vertex(V).

% Constraint: No two vertices in the set can be connected by an edge
:- in_set(U), in_set(V), edge(U, V).

% Objective: Maximize the number of vertices in the independent set
#maximize { 1, V : in_set(V) }.

#show in_set/1.