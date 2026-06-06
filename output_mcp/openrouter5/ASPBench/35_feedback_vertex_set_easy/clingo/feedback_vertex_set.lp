% Directed graph feedback vertex set problem
% Vertices: 1..6
vertex(1..6).

% Edges (directed)
edge(1,2). edge(1,3).
edge(2,4). edge(2,5).
edge(3,4). edge(3,6).
edge(4,2). edge(4,5).
edge(5,3). edge(5,6).
edge(6,1). edge(6,4).

% Choice: which vertices to remove
{ removed(V) } :- vertex(V).

% A vertex that is not removed is "kept"
kept(V) :- vertex(V), not removed(V).

% An edge exists in the reduced graph only if both endpoints are kept
reduced_edge(U,V) :- edge(U,V), kept(U), kept(V).

% Detect cycles in the reduced graph using reachability
% reachable(U,V) means there is a directed path from U to V using reduced edges
reachable(U,V) :- reduced_edge(U,V).
reachable(U,V) :- reachable(U,W), reduced_edge(W,V).

% Constraint: No directed cycle in the reduced graph
% A cycle exists if a vertex can reach itself
:- kept(V), reachable(V,V).

% Minimize the number of removed vertices
#minimize { 1,V : removed(V) }.

#show removed/1.