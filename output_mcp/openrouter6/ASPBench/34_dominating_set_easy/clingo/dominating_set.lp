% Minimum Dominating Set Problem

% Vertices
vertex(1..7).

% Edges (undirected, both directions)
edge(1,2). edge(2,1).
edge(1,3). edge(3,1).
edge(2,3). edge(3,2).
edge(2,4). edge(4,2).
edge(3,5). edge(5,3).
edge(4,6). edge(6,4).
edge(5,6). edge(6,5).
edge(5,7). edge(7,5).
edge(6,7). edge(7,6).

% Choice: select vertices for dominating set
{ selected(V) } :- vertex(V).

% Domination: a vertex is dominated if it is selected or adjacent to a selected vertex
dominated(V) :- selected(V).
dominated(V) :- selected(U), edge(U,V).

% Every vertex must be dominated
:- vertex(V), not dominated(V).

% Minimize the size of the dominating set
#minimize { 1, V : selected(V) }.

% Compute size
size(N) :- N = #count{ V : selected(V) }.

% Show selected vertices and size
#show selected/1.
#show size/1.