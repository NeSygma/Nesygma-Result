% Vertices
vertex(0..15).

% Costs
cost(2, 3). cost(10, 3). cost(14, 3).
cost(V, 1) :- vertex(V), not cost(V, 3).

% Standard Edges
standard_edge(1,3). standard_edge(1,4). standard_edge(2,6). standard_edge(3,7).
standard_edge(4,8). standard_edge(5,11). standard_edge(6,7). standard_edge(7,12).
standard_edge(8,12). standard_edge(11,13). standard_edge(12,13). standard_edge(13,14).

% Heavy Edges
heavy_edge(0,5). heavy_edge(9,10). heavy_edge(14,15).

% Master Vertices
master(0). master(15).

% Antagonistic Pairs
antagonistic(1,2). antagonistic(8,9).

% Selection
{ selected(V) } :- vertex(V).

% Constraint 1: Standard Edge Coverage
:- standard_edge(U, V), not selected(U), not selected(V).

% Constraint 2: Heavy Edge Coverage
% If neither is master, both must be selected.
:- heavy_edge(U, V), not master(U), not master(V), not selected(U).
:- heavy_edge(U, V), not master(U), not master(V), not selected(V).
% If one is master, the master must be selected.
:- heavy_edge(U, V), master(U), not selected(U).
:- heavy_edge(U, V), master(V), not selected(V).

% Constraint 3: Antagonistic Pairs
:- antagonistic(U, V), selected(U), selected(V).

% Objective: Minimize total cost
total_cost(C) :- C = #sum { Cost, V : selected(V), cost(V, Cost) }.
#minimize { C, V : selected(V), cost(V, C) }.

#show selected/1.
#show total_cost/1.