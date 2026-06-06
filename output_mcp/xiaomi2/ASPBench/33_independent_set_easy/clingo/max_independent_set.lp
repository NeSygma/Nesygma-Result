% Vertices
vertex(1..8).

% Edges (undirected graph - listed both directions)
edge(1,2). edge(2,1).
edge(1,3). edge(3,1).
edge(1,4). edge(4,1).
edge(2,5). edge(5,2).
edge(3,6). edge(6,3).
edge(3,7). edge(7,3).
edge(4,8). edge(8,4).
edge(5,6). edge(6,5).
edge(6,7). edge(7,6).
edge(7,8). edge(8,7).

% Choose which vertices to include in the independent set
{ in_set(V) } :- vertex(V).

% Constraint: No two vertices in the set can be connected by an edge
:- in_set(V1), in_set(V2), edge(V1, V2).

% Maximize the number of vertices in the independent set
#maximize { 1,V : in_set(V) }.

#show in_set/1.