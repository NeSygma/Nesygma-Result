%%% Feedback Vertex Set Problem %%%

% --- Data ---
vertex(1..6).

edge(1,2). edge(1,3).
edge(2,4). edge(2,5).
edge(3,4). edge(3,6).
edge(4,2). edge(4,5).
edge(5,3). edge(5,6).
edge(6,1). edge(6,4).

% --- Decision: Choose vertices to remove ---
{ removed(V) } :- vertex(V).

% --- Derived: remaining vertices and edges ---
remaining(V) :- vertex(V), not removed(V).
remaining_edge(F, T) :- edge(F, T), remaining(F), remaining(T).

% --- Acyclicity check via topological ordering ---
% Assign each remaining vertex a number (order) such that
% for every remaining edge F->T, order(F) < order(T).
% If the graph is acyclic, such an ordering exists.

% Each remaining vertex gets exactly one order value (1..6)
1 { order(V, L) : L = 1..6 } 1 :- remaining(V).

% Constraint: for each remaining edge, source's order < target's order
:- remaining_edge(F, T), order(F, OF), order(T, OT), OF >= OT.

% --- Optimization: Minimize removed vertices ---
#minimize { 1, V : removed(V) }.

% --- Output ---
#show removed/1.