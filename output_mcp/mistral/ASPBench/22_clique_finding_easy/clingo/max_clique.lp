% Define vertices
vertex(0..6).

% Define edges (undirected, so both directions)
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

% Select vertices for the clique
{in_clique(V) : vertex(V)}.

% Clique constraint: every pair of vertices in the clique must be connected by an edge
:- in_clique(U), in_clique(V), U < V, not edge(U,V).

% Maximize the clique size
#maximize { 1@1 : in_clique(V) }.

% Show the clique
#show in_clique/1.