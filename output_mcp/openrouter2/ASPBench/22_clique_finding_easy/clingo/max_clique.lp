% vertices
vertex(0). vertex(1). vertex(2). vertex(3). vertex(4). vertex(5). vertex(6).

% edges (undirected)
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

% choice
{ chosen(V) } :- vertex(V).

% clique constraint
:- chosen(U), chosen(V), U < V, not edge(U,V).

% maximize clique size
#maximize {1 : chosen(V)}.

% clique size
clique_size(N) :- N = #count{V : chosen(V)}.

% clique edges
clique_edge(U,V) :- chosen(U), chosen(V), U < V, edge(U,V).

#show chosen/1.
#show clique_size/1.
#show clique_edge/2.