% Define the vertices of the graph.
vertex(1). vertex(2). vertex(3). vertex(4). vertex(5). vertex(6). vertex(7). vertex(8).

% Define the edges of the graph (undirected).
edge(1, 2). edge(1, 3). edge(1, 4).
edge(2, 5).
edge(3, 6). edge(3, 7).
edge(4, 8).
edge(5, 6).
edge(6, 7).
edge(7, 8).

% Helper predicate for undirected edges (to avoid duplication in constraints).
neighbor(V1, V2) :- edge(V1, V2).
neighbor(V2, V1) :- edge(V1, V2).

% Choice rule: select vertices for the independent set.
{ selected(V) : vertex(V) }.

% Constraint: no two selected vertices can be neighbors (connected by an edge).
:- selected(V1), selected(V2), neighbor(V1, V2), V1 != V2.

% Maximize the number of vertices in the independent set.
#maximize { 1@1, V : selected(V) }.

% Show the selected vertices.
#show selected/1.