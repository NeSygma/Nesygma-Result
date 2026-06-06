% Graph vertices
vertex(1). vertex(2). vertex(3). vertex(4).
vertex(5). vertex(6). vertex(7). vertex(8).

% Edges (undirected - store each edge once with smaller vertex first)
edge(1,2). edge(1,3). edge(1,4).
edge(2,5).
edge(3,6). edge(3,7).
edge(4,8).
edge(5,6).
edge(6,7).
edge(7,8).

% Symmetric edge relation
edge(X,Y) :- edge(Y,X).

% Choice: each vertex may or may not be in the independent set
{in_set(X)} :- vertex(X).

% Constraint: No two adjacent vertices can both be in the set
:- in_set(X), in_set(Y), edge(X,Y), X < Y.

% Maximize the number of vertices in the independent set
#maximize { 1,X : in_set(X) }.

% Show the selected vertices
#show in_set/1.