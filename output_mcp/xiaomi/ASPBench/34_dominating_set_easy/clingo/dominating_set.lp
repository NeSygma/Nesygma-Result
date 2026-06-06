% Vertices
vertex(1..7).

% Edges (undirected, listed both ways as given)
edge(1,2). edge(1,3).
edge(2,1). edge(2,3). edge(2,4).
edge(3,1). edge(3,2). edge(3,5).
edge(4,2). edge(4,6).
edge(5,3). edge(5,6). edge(5,7).
edge(6,4). edge(6,5). edge(6,7).
edge(7,5). edge(7,6).

% Choice: each vertex may or may not be in the dominating set
{in_set(V)} :- vertex(V).

% A vertex is dominated if it's in the set OR adjacent to a vertex in the set
dominated(V) :- in_set(V).
dominated(V) :- in_set(U), edge(U, V).

% Constraint: every vertex must be dominated
:- vertex(V), not dominated(V).

% Compute the size of the dominating set
size(N) :- N = #count{V : in_set(V)}.

% Minimize the size of the dominating set
#minimize{N : size(N)}.

% Output
#show in_set/1.
#show size/1.