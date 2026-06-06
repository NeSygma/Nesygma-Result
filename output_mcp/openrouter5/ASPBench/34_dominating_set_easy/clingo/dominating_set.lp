% Graph vertices
vertex(1..7).

% Edges (undirected)
edge(1,2). edge(1,3).
edge(2,1). edge(2,3). edge(2,4).
edge(3,1). edge(3,2). edge(3,5).
edge(4,2). edge(4,6).
edge(5,3). edge(5,6). edge(5,7).
edge(6,4). edge(6,5). edge(6,7).
edge(7,5). edge(7,6).

% Adjacency: symmetric
adj(X,Y) :- edge(X,Y).
adj(X,Y) :- edge(Y,X).

% Choice: which vertices are in the dominating set
{ in_set(V) : vertex(V) }.

% Constraint: every vertex must be in the set or adjacent to a vertex in the set
dominated(V) :- in_set(V).
dominated(V) :- adj(V, U), in_set(U).
:- vertex(V), not dominated(V).

% No vertex can appear more than once (implicitly satisfied by choice rule)

% Minimize the size of the dominating set
#minimize { 1,V : in_set(V) }.

% Output
dominating_set(V) :- in_set(V).
size(N) :- N = #count { V : in_set(V) }.

#show dominating_set/1.
#show size/1.