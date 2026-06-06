% Largest Clique Problem

% Vertices
vertex(0..6).

% Edges (undirected, store both directions)
edge(0,1). edge(1,0).
edge(0,2). edge(2,0).
edge(0,3). edge(3,0).
edge(1,2). edge(2,1).
edge(1,3). edge(3,1).
edge(1,4). edge(4,1).
edge(2,3). edge(3,2).
edge(2,5). edge(5,2).
edge(3,4). edge(4,3).
edge(3,5). edge(5,3).
edge(4,5). edge(5,4).
edge(4,6). edge(6,4).
edge(5,6). edge(6,5).

% Clique vertices: choose any subset
{ clique(V) } :- vertex(V).

% Constraint: all clique vertices must be pairwise connected
:- clique(U), clique(V), U != V, not edge(U,V).

% Compute clique size
clique_size(N) :- N = #count{ V : clique(V) }.

% Maximize clique size
#maximize { 1 : clique_size(N) }.

% Show results
#show clique/1.
#show clique_size/1.