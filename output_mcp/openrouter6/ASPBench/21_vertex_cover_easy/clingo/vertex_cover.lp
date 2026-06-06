% Vertex Cover Problem

% Domain: vertices
vertex(0). vertex(1). vertex(2). vertex(3). vertex(4). vertex(5).

% Edges (undirected, store with u < v)
edge(0,1). edge(0,2). edge(1,3). edge(2,3). edge(2,4). edge(3,5). edge(4,5). edge(1,5).

% Choice: each vertex can be selected or not
{ selected(V) } :- vertex(V).

% Constraint: every edge must be covered (at least one endpoint selected)
:- edge(U,V), not selected(U), not selected(V).

% Minimize the number of selected vertices
#minimize { 1,V : selected(V) }.

% Output: vertex cover array (sorted)
vertex_cover(V) :- selected(V).

% Output: cover size
cover_size(N) :- N = #count{ V : selected(V) }.

% Output: covered edges (all edges are covered by definition)
covered_edge(U,V) :- edge(U,V), U < V.

% Show the required output
#show vertex_cover/1.
#show cover_size/1.
#show covered_edge/2.