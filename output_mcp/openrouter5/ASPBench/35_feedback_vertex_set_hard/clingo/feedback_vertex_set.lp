%% Problem: Minimum-cost Feedback Vertex Set
%% Directed graph with protected vertices, group constraints, and conditional edges

%% Domain
vertex(1..15).

%% Vertex costs
cost(1,10). cost(2,4). cost(3,5). cost(4,6).
cost(5,7). cost(6,9). cost(7,8).
cost(8,2). cost(9,4). cost(10,3).
cost(11,5). cost(12,7). cost(13,6).
cost(14,6). cost(15,12).

%% Protected vertices (cannot be removed)
protected(1). protected(15).

%% Groups
group(a,2). group(a,3). group(a,4).
group(b,5). group(b,6). group(b,7).
group(c,8). group(c,9). group(c,10).
group(d,11). group(d,12). group(d,13).
group(e,14).

%% Core edges (always present if both endpoints remain)
core_edge(1,2). core_edge(1,5). core_edge(1,8).
core_edge(2,3). core_edge(3,4). core_edge(4,2).
core_edge(5,6). core_edge(6,7). core_edge(7,5).
core_edge(8,9). core_edge(9,10). core_edge(10,8).
core_edge(11,12). core_edge(12,13). core_edge(13,11).
core_edge(2,11). core_edge(4,14). core_edge(7,14). core_edge(10,15).
core_edge(14,1).

%% Conditional edges (present only if source vertex is NOT removed)
cond_edge(3,7). cond_edge(3,11).
cond_edge(6,10). cond_edge(6,13).
cond_edge(9,13). cond_edge(9,14).
cond_edge(12,4). cond_edge(12,7).

%% Decision: which vertices to remove
{ removed(V) } :- vertex(V), not protected(V).

%% Constraint 3: At most one vertex per group can be removed
:- group(G,V1), group(G,V2), V1 != V2, removed(V1), removed(V2).

%% Constraint 2: Protected vertices cannot be removed
:- removed(V), protected(V).

%% Define which edges exist in the remaining graph
%% Core edges exist if both endpoints remain
edge(V1,V2) :- core_edge(V1,V2), not removed(V1), not removed(V2).

%% Conditional edges exist if source is not removed and both endpoints remain
edge(V1,V2) :- cond_edge(V1,V2), not removed(V1), not removed(V2).

%% Constraint 1: Acyclicity - no directed cycles in remaining graph
%% Use reachability to detect cycles
%% reachable(X,Y) means there is a directed path from X to Y
reachable(X,Y) :- edge(X,Y).
reachable(X,Y) :- reachable(X,Z), edge(Z,Y), vertex(X), vertex(Y), vertex(Z).

%% A cycle exists if there is an edge from X to Y and Y can reach X
%% But we need to be careful: a self-loop is also a cycle
cycle :- edge(X,Y), reachable(Y,X).
cycle :- edge(X,X).

:- cycle.

%% Objective: Minimize total removal cost
total_cost(C) :- C = #sum { Cost, V : removed(V), cost(V,Cost) }.

%% For showing the solution
#show removed/1.
#show total_cost/1.