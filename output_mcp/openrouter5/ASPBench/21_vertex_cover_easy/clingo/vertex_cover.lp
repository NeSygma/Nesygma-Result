% Vertex Cover Problem - Minimum Vertex Cover

% Instance Data
vertex(0..5).

% Edges (undirected, stored with u < v)
edge(0,1).
edge(0,2).
edge(1,3).
edge(2,3).
edge(2,4).
edge(3,5).
edge(4,5).
edge(1,5).

% Choice: select a subset of vertices
{ selected(V) } :- vertex(V).

% Constraint: Every edge must be covered by at least one selected vertex
:- edge(U,V), not selected(U), not selected(V).

% Objective: Minimize the number of selected vertices
#minimize { 1,V : selected(V) }.

% Output
#show selected/1.
#show cover_size/1.
cover_size(N) :- N = #count { V : selected(V) }.