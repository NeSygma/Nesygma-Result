% Domain
vertex(0). vertex(1). vertex(2). vertex(3). vertex(4). vertex(5).

edge(0,1). edge(0,2). edge(1,3). edge(2,3). edge(2,4). edge(3,5). edge(4,5). edge(1,5).

% Choose vertices for the cover
{ selected(V) : vertex(V) }.

% Each edge must be incident to a selected vertex
:- edge(U,V), not selected(U), not selected(V).

% Minimize the number of selected vertices
#minimize { V : selected(V) }.

% Compute cover size
cover_size(N) :- #count{ V : selected(V) } = N.

% Compute covered edges
covered_edge(U,V) :- edge(U,V), selected(U).
covered_edge(U,V) :- edge(U,V), selected(V).

% Output
#show selected/1.
#show cover_size/1.
#show covered_edge/2.