% Feedback Vertex Set Problem
% Find minimum set of vertices whose removal makes the directed graph acyclic.

% Vertices
vertex(1..6).

% Directed edges
edge(1,2). edge(1,3).
edge(2,4). edge(2,5).
edge(3,4). edge(3,6).
edge(4,2). edge(4,5).
edge(5,3). edge(5,6).
edge(6,1). edge(6,4).

% Choice: which vertices are removed
{removed(V)} :- vertex(V).

% Remaining vertices (not removed)
remaining(V) :- vertex(V), not removed(V).

% Remaining edges (both endpoints remain)
remaining_edge(U,V) :- edge(U,V), remaining(U), remaining(V).

% Assign a topological order to each vertex (1..6)
% Each vertex gets exactly one order value
1 {order(V, K) : K=1..6} 1 :- vertex(V).

% For each remaining edge, enforce order(u) < order(v)
:- remaining_edge(U,V), order(U, K1), order(V, K2), K1 >= K2.

% Minimize the number of removed vertices
#minimize {1, V : removed(V)}.

% Show the removed vertices
#show removed/1.