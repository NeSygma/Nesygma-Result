% Define the vertices
vertex(0..15).

% Vertex costs: high-cost vertices (cost 3) and others (cost 1)
cost(2, 3).  cost(10, 3).  cost(14, 3).
cost(0, 1).  cost(1, 1).  cost(3, 1).  cost(4, 1).  cost(5, 1).
cost(6, 1).  cost(7, 1).  cost(8, 1).  cost(9, 1).  cost(11, 1).
cost(12, 1).  cost(13, 1).  cost(15, 1).

% Standard edges
standard_edge(1,3). standard_edge(1,4). standard_edge(2,6).
standard_edge(3,7). standard_edge(4,8). standard_edge(5,11).
standard_edge(6,7). standard_edge(7,12). standard_edge(8,12).
standard_edge(11,13). standard_edge(12,13). standard_edge(13,14).

% Heavy edges
heavy_edge(0,5). heavy_edge(9,10). heavy_edge(14,15).

% Master vertices
master_vertex(0). master_vertex(15).

% Antagonistic pairs
antagonistic_pair(1,2). antagonistic_pair(8,9).

% Choice rule: select vertices
{ selected(V) : vertex(V) }.

% Standard edge coverage: at least one endpoint must be selected
covered_standard(U, V) :- selected(U), standard_edge(U, V).
covered_standard(U, V) :- selected(V), standard_edge(U, V).

% Heavy edge coverage rules:
% 1. Both endpoints selected
covered_heavy(U, V) :- selected(U), selected(V), heavy_edge(U, V).
% 2. Master vertex exception: only the master vertex needs to be selected
covered_heavy(U, V) :- master_vertex(U), selected(U), heavy_edge(U, V).
covered_heavy(U, V) :- master_vertex(V), selected(V), heavy_edge(U, V).

% Ensure all standard edges are covered
:- standard_edge(U, V), not covered_standard(U, V).

% Ensure all heavy edges are covered
:- heavy_edge(U, V), not covered_heavy(U, V).

% Antagonistic pairs: at most one can be selected
:- selected(U), selected(V), antagonistic_pair(U, V).

% Calculate total cost
selected_cost(C) :- selected(V), cost(V, C).
total_cost(S) :- S = #sum { C : selected_cost(C) }.

% Minimize total cost
#minimize { C : selected_cost(C) }.

% Show the solution
#show selected/1.
#show total_cost/1.