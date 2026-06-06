% vertices
vertex(0..5).

% edges (u<v)
edge(0,1).
edge(0,2).
edge(1,3).
edge(2,3).
edge(2,4).
edge(3,5).
edge(4,5).
edge(1,5).

% choice of selected vertices
{selected(V)} :- vertex(V).

% each edge must be covered
:- edge(U,V), not selected(U), not selected(V).

% define cover size
cover_size(N) :- N = #count { V : selected(V) }.

% define vertex_cover for output
vertex_cover(V) :- selected(V).

% define covered edges (ensure u<v)
covered_edge(U,V) :- edge(U,V), selected(U).
covered_edge(U,V) :- edge(U,V), selected(V).

% optimization: minimize size then sum of indices
#minimize { 1,V : selected(V) }.
#minimize { V,V : selected(V) }.

#show vertex_cover/1.
#show cover_size/1.
#show covered_edge/2.