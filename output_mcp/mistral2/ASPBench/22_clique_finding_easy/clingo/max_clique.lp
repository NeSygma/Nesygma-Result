% Declare vertices
vertex(0..6).

% Declare edges (undirected, so both directions)
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

% Choice rule: select vertices for the clique
{in_clique(V) : vertex(V)}.

% Ensure all pairs in the clique are connected by an edge
:- in_clique(U), in_clique(V), U < V, not edge(U,V).

% Calculate the size of the clique
clique_size(N) :- N = #count{V : in_clique(V)}.

% Maximize the clique size
#maximize {N : clique_size(N)}.

% Show the clique vertices and size
#show in_clique/1.
#show clique_size/1.