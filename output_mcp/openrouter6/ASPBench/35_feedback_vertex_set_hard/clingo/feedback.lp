% Feedback Vertex Set Problem
% Vertices 1-15 with costs and constraints

% ===== 1. DOMAIN DEFINITIONS =====
vertex(1..15).

% Costs for each vertex
cost(1, 10). cost(2, 4). cost(3, 5). cost(4, 6).
cost(5, 7). cost(6, 9). cost(7, 8).
cost(8, 2). cost(9, 4). cost(10, 3).
cost(11, 5). cost(12, 7). cost(13, 6).
cost(14, 6). cost(15, 12).

% Protected vertices (cannot be removed)
protected(1).
protected(15).

% ===== 2. GROUP DEFINITIONS =====
% Group A: {2, 3, 4}
group(a, 2). group(a, 3). group(a, 4).
% Group B: {5, 6, 7}
group(b, 5). group(b, 6). group(b, 7).
% Group C: {8, 9, 10}
group(c, 8). group(c, 9). group(c, 10).
% Group D: {11, 12, 13}
group(d, 11). group(d, 12). group(d, 13).
% Group E: {14}
group(e, 14).

% ===== 3. CORE EDGES (always present) =====
core_edge(1, 2). core_edge(1, 5). core_edge(1, 8).
core_edge(2, 3). core_edge(3, 4). core_edge(4, 2).
core_edge(5, 6). core_edge(6, 7). core_edge(7, 5).
core_edge(8, 9). core_edge(9, 10). core_edge(10, 8).
core_edge(11, 12). core_edge(12, 13). core_edge(13, 11).
core_edge(2, 11). core_edge(4, 14). core_edge(7, 14). core_edge(10, 15).
core_edge(14, 1).

% ===== 4. CONDITIONAL EDGES (present only if source remains) =====
% If 3 remains: 3→7, 3→11
conditional_edge(3, 7) :- remaining(3).
conditional_edge(3, 11) :- remaining(3).
% If 6 remains: 6→10, 6→13
conditional_edge(6, 10) :- remaining(6).
conditional_edge(6, 13) :- remaining(6).
% If 9 remains: 9→13, 9→14
conditional_edge(9, 13) :- remaining(9).
conditional_edge(9, 14) :- remaining(9).
% If 12 remains: 12→4, 12→7
conditional_edge(12, 4) :- remaining(12).
conditional_edge(12, 7) :- remaining(12).

% ===== 5. DECISION VARIABLES =====
% Choose which vertices to remove (0 or 1 for each vertex)
{ removed(V) } :- vertex(V).

% Protected vertices cannot be removed
:- removed(V), protected(V).

% Group constraint: at most one vertex per group can be removed
% For each group, sum of removed vertices in that group ≤ 1
:- #count{ V : removed(V), group(G, V) } > 1, group(G, _).

% ===== 6. DERIVED PREDICATES =====
% Remaining vertices are those not removed
remaining(V) :- vertex(V), not removed(V).

% Edge exists in remaining graph if both endpoints remain and edge is present
edge(U, V) :- remaining(U), remaining(V), core_edge(U, V).
edge(U, V) :- remaining(U), remaining(V), conditional_edge(U, V).

% ===== 7. ACYCLICITY CONSTRAINT =====
% Assign an order to each remaining vertex (1 to 15)
{ order(V, O) : O = 1..15 } 1 :- remaining(V).

% For each edge, the source must have a lower order than the target
:- edge(U, V), order(U, OU), order(V, OV), OU >= OV.

% ===== 8. OBJECTIVE FUNCTION =====
% Minimize total removal cost
#minimize { C, V : removed(V), cost(V, C) }.

% ===== 9. OUTPUT PREDICATES =====
% Feedback set (vertices to remove)
feedback_vertex(V) :- removed(V).

% Costs for each removed vertex
feedback_cost(V, C) :- removed(V), cost(V, C).

% Total cost
total_cost(T) :- T = #sum{ C, V : removed(V), cost(V, C) }.

% Remaining vertices
remaining_vertex(V) :- remaining(V).

% ===== 10. SHOW DIRECTIVES =====
#show feedback_vertex/1.
#show feedback_cost/2.
#show total_cost/1.
#show remaining_vertex/1.