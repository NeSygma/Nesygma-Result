% vertices
vertex(1..8).
% edges (undirected, both directions)
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

% choice of vertices in independent set
{ in(V) } :- vertex(V).

% independence constraint: no edge between two selected vertices
:- in(V), in(U), edge(V,U), V < U.

% maximize size of independent set
#maximize { 1, V : in(V) }.

#show in/1.