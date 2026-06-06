% Vertex Cover with Special Constraints

% Domains
vertex(0..15).

% Costs
cost(2,3). cost(10,3). cost(14,3).
cost(V,1) :- vertex(V), V != 2, V != 10, V != 14.

% Standard edges
standard_edge(1,3). standard_edge(1,4). standard_edge(2,6). standard_edge(3,7).
standard_edge(4,8). standard_edge(5,11). standard_edge(6,7). standard_edge(7,12).
standard_edge(8,12). standard_edge(11,13). standard_edge(12,13). standard_edge(13,14).

% Heavy edges
heavy_edge(0,5). heavy_edge(9,10). heavy_edge(14,15).

% Master vertices
master(0). master(15).

% Antagonistic pairs
antagonistic(1,2). antagonistic(8,9).

% Choice rule: select vertices
{ selected(V) } :- vertex(V).

% Constraint 1: Standard edge coverage
:- standard_edge(U,V), not selected(U), not selected(V).

% Constraint 2: Heavy edge coverage
% Define covered_heavy predicate
covered_heavy(U,V) :- heavy_edge(U,V), selected(U), selected(V).
covered_heavy(U,V) :- heavy_edge(U,V), master(U), selected(U).
covered_heavy(U,V) :- heavy_edge(U,V), master(V), selected(V).
:- heavy_edge(U,V), not covered_heavy(U,V).

% Constraint 3: Antagonistic pairs
:- antagonistic(U,V), selected(U), selected(V).

% Objective: minimize total cost
#minimize { C, V : selected(V), cost(V,C) }.

% Compute total cost for display
total_cost(N) :- N = #sum { C,V : selected(V), cost(V,C) }.

% Show selected vertices and total cost
#show selected/1.
#show total_cost/1.