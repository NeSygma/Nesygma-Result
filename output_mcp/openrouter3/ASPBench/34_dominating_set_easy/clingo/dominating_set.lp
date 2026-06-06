% Minimum Dominating Set Problem

% Domain: vertices 1-7
vertex(1..7).

% Edges (undirected graph)
edge(1,2). edge(2,1).
edge(1,3). edge(3,1).
edge(2,3). edge(3,2).
edge(2,4). edge(4,2).
edge(3,5). edge(5,3).
edge(4,6). edge(6,4).
edge(5,6). edge(6,5).
edge(5,7). edge(7,5).
edge(6,7). edge(7,6).

% Choice rule: each vertex can be in the dominating set or not
% We want to minimize the number of vertices in the set
{ in_set(V) } :- vertex(V).

% A vertex is dominated if it's in the set OR adjacent to a vertex in the set
dominated(V) :- in_set(V).
dominated(V) :- vertex(V), edge(V, U), in_set(U).

% Constraint: every vertex must be dominated
:- vertex(V), not dominated(V).

% Calculate the size of the dominating set
size(N) :- N = #count{ V : in_set(V) }.

% Minimize the size of the dominating set
#minimize { N : size(N) }.

% Output: dominating set (sorted) and size
dominating_set(V) :- in_set(V).
optimal_size(N) :- size(N).

% Show only the output predicates
#show dominating_set/1.
#show optimal_size/1.