% Declare all vertices
vertex(1..8).

% Declare all edges (undirected)
edge(1,2). edge(1,3). edge(1,4).
edge(2,5).
edge(3,6). edge(3,7).
edge(4,8).
edge(5,6).
edge(6,7).
edge(7,8).

% Allow selection of vertices for the independent set
{ in_set(V) : vertex(V) }.

% Ensure no two adjacent vertices are in the set
:- edge(U, V), in_set(U), in_set(V).

% Maximize the size of the independent set
#maximize { 1@1 : in_set(V) }.

% Show the selected vertices
#show in_set/1.