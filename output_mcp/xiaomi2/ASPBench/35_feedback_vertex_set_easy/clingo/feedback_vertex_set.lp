% Vertices
vertex(1). vertex(2). vertex(3). vertex(4). vertex(5). vertex(6).

% Directed edges
edge(1,2). edge(1,3).
edge(2,4). edge(2,5).
edge(3,4). edge(3,6).
edge(4,2). edge(4,5).
edge(5,3). edge(5,6).
edge(6,1). edge(6,4).

% Choice: which vertices to remove
{ remove(V) } :- vertex(V).

% Remaining vertices (not removed)
remaining(V) :- vertex(V), not remove(V).

% Remaining edges: both endpoints must remain
remains(U,V) :- edge(U,V), remaining(U), remaining(V).

% Topological ordering domain
order(1..6).

% Each remaining vertex gets exactly one order number
1 { assign(V, O) : order(O) } 1 :- remaining(V).

% No two remaining vertices share the same order
:- assign(V1, O), assign(V2, O), V1 != V2.

% For every remaining edge (U,V), order(U) must be < order(V)
% This guarantees acyclicity
:- remains(U,V), assign(U, O1), assign(V, O2), O1 >= O2.

% Minimize the number of removed vertices
#minimize { 1, V : remove(V) }.

#show remove/1.