% Maximum Clique Problem

% Define vertices
vertex(0). vertex(1). vertex(2). vertex(3). vertex(4). vertex(5). vertex(6).

% Define edges (undirected graph)
edge(0, 1). edge(0, 2). edge(0, 3).
edge(1, 2). edge(1, 3). edge(1, 4).
edge(2, 3). edge(2, 5).
edge(3, 4). edge(3, 5).
edge(4, 5). edge(4, 6).
edge(5, 6).

% Symmetric edges (since graph is undirected)
edge(V, U) :- edge(U, V).

% Choice rule: select vertices for the clique
{ clique(V) } :- vertex(V).

% Constraint: all selected vertices must be pairwise connected
:- clique(U), clique(V), U != V, not edge(U, V).

% Count clique size
clique_size(N) :- N = #count { V : clique(V) }.

% Show the clique vertices and size
#show clique/1.
#show clique_size/1.

% Optimization: maximize clique size
#maximize { 1, V : clique(V) }.