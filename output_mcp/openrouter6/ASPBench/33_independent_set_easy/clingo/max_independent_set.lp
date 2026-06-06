% Maximum Independent Set in a Graph

% Vertices
vertex(1..8).

% Edges (undirected, unique pairs)
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

% Choice: select a vertex for the independent set
{ selected(V) } :- vertex(V).

% Independence constraint: no two selected vertices are adjacent
:- selected(U), selected(V), edge(U,V), U != V.

% Objective: maximize the number of selected vertices
#maximize { 1, V : selected(V) }.

% Show the selected vertices and the size
#show selected/1.
#show size/1.
size(N) :- N = #count{ V : selected(V) }.
#show size/1.