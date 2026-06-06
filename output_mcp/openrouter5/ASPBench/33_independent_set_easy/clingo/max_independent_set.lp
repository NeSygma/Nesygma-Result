% Graph vertices
vertex(1..8).

% Edges (undirected - each edge listed once)
edge(1,2). edge(1,3). edge(1,4).
edge(2,5).
edge(3,6). edge(3,7).
edge(4,8).
edge(5,6).
edge(6,7).
edge(7,8).

% Make edges symmetric for easier constraint checking
adj(X,Y) :- edge(X,Y).
adj(Y,X) :- edge(X,Y).

% Choice: each vertex can be in the independent set or not
{ in_set(V) } :- vertex(V).

% Constraint: no two adjacent vertices can both be in the set
:- in_set(V1), in_set(V2), adj(V1,V2), V1 < V2.

% Maximize the number of vertices in the independent set
#maximize { 1,V : in_set(V) }.

#show in_set/1.
#show size/1.

% Compute the size of the independent set
size(N) :- N = #count { V : in_set(V) }.