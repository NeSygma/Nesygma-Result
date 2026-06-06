% Define the vertices and edges of the graph.
vertex(1..7).

edge(1, 2). edge(1, 3).
edge(2, 1). edge(2, 3). edge(2, 4).
edge(3, 1). edge(3, 2). edge(3, 5).
edge(4, 2). edge(4, 6).
edge(5, 3). edge(5, 6). edge(5, 7).
edge(6, 4). edge(6, 5). edge(6, 7).
edge(7, 5). edge(7, 6).

% Symmetric edges (undirected graph)
edge(U, V) :- edge(V, U).

% Choice rule: select vertices for the dominating set
{ in_set(V) : vertex(V) }.

% Constraint: Every vertex must be in the set or adjacent to a vertex in the set
:- vertex(V), not in_set(V), not adjacent_to_set(V).

% Helper: A vertex is adjacent to the set if it is adjacent to a vertex in the set
adjacent_to_set(V) :- edge(V, U), in_set(U).

% Optimization: Minimize the size of the dominating set
#minimize { 1@1, V : in_set(V) }.

% Output the dominating set and its size
size(S) :- S = #count{ V : in_set(V) }.

#show in_set/1.
#show size/1.