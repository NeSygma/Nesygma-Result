% --- Instance Data ---
vertex(1..6).
edge(1,2). edge(1,3).
edge(2,4). edge(2,5).
edge(3,4). edge(3,6).
edge(4,2). edge(4,5).
edge(5,3). edge(5,6).
edge(6,1). edge(6,4).

% --- Logic ---
% Choice: Decide which vertices to remove
{ removed(V) } :- vertex(V).

% Define remaining vertices and edges
remaining(V) :- vertex(V), not removed(V).
remaining_edge(U, V) :- edge(U, V), remaining(U), remaining(V).

% Reachability in the remaining graph
reachable(U, V) :- remaining_edge(U, V).
reachable(U, W) :- reachable(U, V), remaining_edge(V, W).

% Constraint: No cycles (a vertex cannot reach itself)
:- reachable(V, V).

% Objective: Minimize the number of removed vertices
#minimize { 1, V : removed(V) }.

% Output
#show removed/1.