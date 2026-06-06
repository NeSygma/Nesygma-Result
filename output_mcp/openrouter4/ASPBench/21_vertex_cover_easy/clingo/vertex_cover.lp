% Domain
vertex(0..5).

% Edges (undirected, listed once with u < v)
edge(0,1). edge(0,2). edge(1,3). edge(2,3).
edge(2,4). edge(3,5). edge(4,5). edge(1,5).

% Choice: select a vertex cover
{ selected(V) } :- vertex(V).

% Constraint: every edge must be covered
covered(edge(U,V)) :- selected(U), edge(U,V).
covered(edge(U,V)) :- selected(V), edge(U,V).
:- edge(U,V), not covered(edge(U,V)).

% Derive cover size
cover_size(N) :- N = #count { V : selected(V) }.

% Objective: minimize the number of selected vertices
#minimize { 1@1,V : selected(V) }.

% Output
#show selected/1.
#show cover_size/1.