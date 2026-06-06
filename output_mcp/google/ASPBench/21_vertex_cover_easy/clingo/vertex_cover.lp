% Vertices
vertex(0..5).

% Edges
edge(0, 1).
edge(0, 2).
edge(1, 3).
edge(2, 3).
edge(2, 4).
edge(3, 5).
edge(4, 5).
edge(1, 5).

% Choice rule: select a subset of vertices
{ selected(V) } :- vertex(V).

% Constraint: Every edge must be covered by at least one selected vertex
:- edge(U, V), not selected(U), not selected(V).

% Objective: Minimize the number of selected vertices
#minimize { 1, V : selected(V) }.

% Output formatting
vertex_cover(V) :- selected(V).
cover_size(N) :- N = #count { V : selected(V) }.
covered_edge(U, V) :- edge(U, V).

#show vertex_cover/1.
#show cover_size/1.
#show covered_edge/2.