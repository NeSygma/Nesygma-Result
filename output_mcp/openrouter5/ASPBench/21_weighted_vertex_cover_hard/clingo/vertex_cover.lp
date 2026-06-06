% Vertex Cover Problem - Minimum Cost

% --- Domain Definitions ---
vertex(0..15).

% Vertex Costs
cost(2, 3). cost(10, 3). cost(14, 3).
cost(V, 1) :- vertex(V), V != 2, V != 10, V != 14.

% Standard Edges
standard_edge(1,3). standard_edge(1,4). standard_edge(2,6).
standard_edge(3,7). standard_edge(4,8). standard_edge(5,11).
standard_edge(6,7). standard_edge(7,12). standard_edge(8,12).
standard_edge(11,13). standard_edge(12,13). standard_edge(13,14).

% Heavy Edges
heavy_edge(0,5). heavy_edge(9,10). heavy_edge(14,15).

% Master Vertices
master(0). master(15).

% Antagonistic Pairs
antagonistic(1,2). antagonistic(8,9).

% --- Decision: Select vertices ---
{ selected(V) } :- vertex(V).

% --- Constraint 1: Standard Edge Coverage ---
% At least one endpoint of each standard edge must be selected
:- standard_edge(U, V), not selected(U), not selected(V).

% --- Constraint 2: Heavy Edge Coverage ---
% General rule: both endpoints must be selected
% Exception: if one endpoint is a master, selecting just the master is enough

% A heavy edge is covered if:
% (a) both endpoints are selected, OR
% (b) one endpoint is a master and that master is selected

% For each heavy edge, it must be covered
:- heavy_edge(U, V), not covered_heavy(U, V).

% Covered if both endpoints selected
covered_heavy(U, V) :- heavy_edge(U, V), selected(U), selected(V).

% Covered if U is master and U is selected
covered_heavy(U, V) :- heavy_edge(U, V), master(U), selected(U).

% Covered if V is master and V is selected
covered_heavy(U, V) :- heavy_edge(U, V), master(V), selected(V).

% --- Constraint 3: Antagonistic Pairs ---
% Cannot select both vertices from an antagonistic pair
:- antagonistic(U, V), selected(U), selected(V).

% --- Objective: Minimize total cost ---
% Compute total cost
total_cost(C) :- C = #sum { Cost, V : selected(V), cost(V, Cost) }.

% Minimize total cost
#minimize { Cost, V : selected(V), cost(V, Cost) }.

% --- Output ---
#show selected/1.
#show total_cost/1.