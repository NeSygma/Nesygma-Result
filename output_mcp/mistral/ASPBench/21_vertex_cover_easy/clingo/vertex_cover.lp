% Define the vertices
vertex(0..5).

% Define the edges as facts (undirected, so store both orders for safety)
edge(0, 1). edge(1, 0).
edge(0, 2). edge(2, 0).
edge(1, 3). edge(3, 1).
edge(2, 3). edge(3, 2).
edge(2, 4). edge(4, 2).
edge(3, 5). edge(5, 3).
edge(4, 5). edge(5, 4).
edge(1, 5). edge(5, 1).

% Choice rule: select vertices for the cover
{ selected(V) : vertex(V) }.

% Ensure every edge is covered by at least one selected vertex
:- edge(U, V), not selected(U), not selected(V).

% Minimize the number of selected vertices
#minimize { V : selected(V) }.

% Show the selected vertices and cover size
#show selected/1.
#show cover_size/1.

% Helper to compute cover size
cover_size(N) :- N = #count{ V : selected(V) }.

% Ensure cover_size is shown
:- not cover_size(_).