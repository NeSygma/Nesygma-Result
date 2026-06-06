% Vertices
vertex(0). vertex(1). vertex(2). vertex(3). vertex(4). vertex(5).

% Edges (undirected, u < v)
edge(0,1). edge(0,2). edge(1,3). edge(2,3). edge(2,4). edge(3,5). edge(4,5). edge(1,5).

% Choice rule: select any subset of vertices
{selected(V)} :- vertex(V).

% Constraint: every edge must be incident to a selected vertex
:- edge(U,V), not selected(U), not selected(V).

% Objective: minimize number of selected vertices
#minimize {1@1, V : selected(V)}.

% Derived predicates for output
cover_size(N) :- N = #count{V : selected(V)}.
vertex_cover(V) :- selected(V).
covered_edges(U,V) :- edge(U,V).

#show cover_size/1.
#show vertex_cover/1.
#show covered_edges/2.