% Vertices
vertex(0..6).

% Edges (undirected - stored both directions for easy lookup)
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

% Choose which vertices are in the clique
{ in_clique(V) } :- vertex(V).

% Constraint: every pair of vertices in the clique must be connected
:- in_clique(U), in_clique(V), U < V, not edge(U, V).

% Count clique size
clique_size(N) :- N = #count{V : in_clique(V)}.

% Count edges within the clique
clique_edges(M) :- M = #count{U,V : in_clique(U), in_clique(V), U < V, edge(U,V)}.

% Maximize clique size
#maximize { N : clique_size(N) }.

#show in_clique/1.
#show clique_size/1.
#show clique_edges/1.