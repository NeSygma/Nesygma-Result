% Domain
vertex(0..15).

% Costs
cost(2, 3). cost(10, 3). cost(14, 3).
cost(V, 1) :- vertex(V), V != 2, V != 10, V != 14.

% Standard edges
std_edge(1,3). std_edge(1,4). std_edge(2,6). std_edge(3,7).
std_edge(4,8). std_edge(5,11). std_edge(6,7). std_edge(7,12).
std_edge(8,12). std_edge(11,13). std_edge(12,13). std_edge(13,14).

% Heavy edges
heavy_edge(0,5). heavy_edge(9,10). heavy_edge(14,15).

% Master vertices
master(0). master(15).

% Antagonistic pairs (symmetric)
antag(1,2). antag(8,9).
antag(U, V) :- antag(V, U).

% Choice: select vertices
{ selected(V) } :- vertex(V).

% Constraint 1: Standard edge coverage - at least one endpoint selected
:- std_edge(U, V), not selected(U), not selected(V).

% Constraint 2: Heavy edge coverage
% A heavy edge (U,V) is covered if:
%   - both U and V are selected, OR
%   - U is a master and U is selected, OR
%   - V is a master and V is selected
heavy_covered(U, V) :- heavy_edge(U, V), selected(U), selected(V).
heavy_covered(U, V) :- heavy_edge(U, V), master(U), selected(U).
heavy_covered(U, V) :- heavy_edge(U, V), master(V), selected(V).

% Forbid uncovered heavy edges
:- heavy_edge(U, V), not heavy_covered(U, V).

% Constraint 3: Antagonistic pairs - at most one selected
:- antag(U, V), selected(U), selected(V).

% Objective: minimize total cost
#minimize { C, V : selected(V), cost(V, C) }.

% Compute total cost for display
total_cost(C) :- C = #sum { Cost, V : selected(V), cost(V, Cost) }.

#show selected/1.
#show total_cost/1.