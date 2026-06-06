%% Facts: vertices and edges
vertex(1..7).

edge(1,2). edge(1,3). edge(2,3). edge(2,4). edge(3,5). edge(4,6). edge(5,6). edge(5,7). edge(6,7).

%% Undirected adjacency
adjacent(X,Y) :- edge(X,Y).
adjacent(X,Y) :- edge(Y,X).

%% Choice: which vertices are in the dominating set
{ in_set(V) } :- vertex(V).

%% Domination condition
dominated(V) :- in_set(V).
dominated(V) :- adjacent(V,U), in_set(U).

%% Every vertex must be dominated
:- vertex(V), not dominated(V).

%% Minimize the size of the dominating set
#minimize { 1,V : in_set(V) }.

%% Output
dominating_set(V) :- in_set(V).
size(N) :- N = #count { V : in_set(V) }.
#show dominating_set/1.
#show size/1.