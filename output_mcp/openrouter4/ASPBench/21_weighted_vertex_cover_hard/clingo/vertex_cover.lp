% --- Domains ---
vertex(0..15).

% --- Costs ---
cost(2,3). cost(10,3). cost(14,3).
cost(V,1) :- vertex(V), V != 2, V != 10, V != 14.

% --- Edges ---
standard_edge(1,3). standard_edge(1,4). standard_edge(2,6). 
standard_edge(3,7). standard_edge(4,8). standard_edge(5,11). 
standard_edge(6,7). standard_edge(7,12). standard_edge(8,12). 
standard_edge(11,13). standard_edge(12,13). standard_edge(13,14).

heavy_edge(0,5). heavy_edge(9,10). heavy_edge(14,15).

% --- Master vertices ---
master(0). master(15).

% --- Antagonistic pairs ---
antagonistic(1,2). antagonistic(8,9).

% --- Choice: select vertices ---
{select(V)} :- vertex(V).

% --- Constraint 1: Standard edge coverage (at least one endpoint) ---
:- standard_edge(U,V), not select(U), not select(V).

% --- Constraint 2: Heavy edge coverage ---
% Both unselected -> uncovered
:- heavy_edge(U,V), not select(U), not select(V).
% Only U selected, U not master -> uncovered
:- heavy_edge(U,V), select(U), not select(V), not master(U).
% Only V selected, V not master -> uncovered
:- heavy_edge(U,V), select(V), not select(U), not master(V).

% --- Constraint 3: Antagonistic pairs (at most one selected) ---
:- antagonistic(U,V), select(U), select(V).

% --- Optimization: minimize total cost ---
#minimize{ Cost, V : select(V), cost(V,Cost) }.

% --- Derived total cost for display ---
total_cost(C) :- C = #sum{ Cost, V : select(V), cost(V,Cost) }.

% --- Show results ---
#show select/1.
#show total_cost/1.