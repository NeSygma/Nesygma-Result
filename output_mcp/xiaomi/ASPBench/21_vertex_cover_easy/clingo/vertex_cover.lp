% Domain: vertices
vertex(0). vertex(1). vertex(2). vertex(3). vertex(4). vertex(5).

% Edges (undirected, stored as u < v)
edge(0,1).
edge(0,2).
edge(1,3).
edge(2,3).
edge(2,4).
edge(3,5).
edge(4,5).
edge(1,5).

% Choice: select vertices
{selected(V)} :- vertex(V).

% Constraint: every edge must be covered by at least one selected vertex
:- edge(U,V), not selected(U), not selected(V).

% Minimize the number of selected vertices
#minimize {1,V : selected(V)}.

% Show results
#show selected/1.