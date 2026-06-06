% Vertices
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

% Choice: select each vertex or not
{ in_cover(V) } :- vertex(V).

% Constraint: every edge must be covered by at least one endpoint
:- edge(U,V), not in_cover(U), not in_cover(V).

% Compute cover size
cover_size(N) :- N = #count{V : in_cover(V)}.

% Compute covered edges (all edges are covered by constraint, list them)
covered(U,V) :- edge(U,V), in_cover(U).
covered(U,V) :- edge(U,V), in_cover(V).

% Minimize the number of selected vertices
#minimize { 1,V : in_cover(V) }.

% Output
#show in_cover/1.
#show cover_size/1.
#show covered/2.