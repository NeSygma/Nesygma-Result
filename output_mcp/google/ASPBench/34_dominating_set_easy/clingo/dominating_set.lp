% --- Graph Definition ---
vertex(1..7).

edge(1, 2). edge(2, 1).
edge(1, 3). edge(3, 1).
edge(2, 3). edge(3, 2).
edge(2, 4). edge(4, 2).
edge(3, 5). edge(5, 3).
edge(4, 6). edge(6, 4).
edge(5, 6). edge(6, 5).
edge(5, 7). edge(7, 5).
edge(6, 7). edge(7, 6).

% --- Dominating Set Logic ---
% Choice rule: A vertex is either in the set or not.
{ in_set(V) } :- vertex(V).

% A vertex is dominated if it is in the set or adjacent to a vertex in the set.
dominated(V) :- in_set(V).
dominated(V) :- in_set(U), edge(U, V).

% Constraint: Every vertex must be dominated.
:- vertex(V), not dominated(V).

% --- Objective ---
% Minimize the size of the dominating set.
#minimize { 1, V : in_set(V) }.

% --- Output ---
dominating_set(V) :- in_set(V).
size(N) :- N = #count { V : in_set(V) }.

#show dominating_set/1.
#show size/1.