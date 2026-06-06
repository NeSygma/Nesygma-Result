% vertices
vertex(1..7).
% edges (undirected)
edge(1,2). edge(2,1).
edge(1,3). edge(3,1).
edge(2,3). edge(3,2).
edge(2,4). edge(4,2).
edge(3,5). edge(5,3).
edge(4,6). edge(6,4).
edge(5,6). edge(6,5).
edge(5,7). edge(7,5).
edge(6,7). edge(7,6).

% choice of dominating set vertices
{ in_set(V) } :- vertex(V).

% domination condition
covered(V) :- in_set(V).
covered(V) :- edge(V,U), in_set(U).

% every vertex must be covered
:- vertex(V), not covered(V).

% minimize size, then lexicographically smallest set
#minimize { 1, V : in_set(V) }.

% output
 dominating_set(V) :- in_set(V).
 size(N) :- N = #count { V : in_set(V) }.
#show dominating_set/1.
#show size/1.