% Vertices
vertex(0). vertex(1). vertex(2). vertex(3). vertex(4). vertex(5). vertex(6). vertex(7). vertex(8). vertex(9). vertex(10). vertex(11). vertex(12). vertex(13). vertex(14). vertex(15).

% Costs
cost(2,3). cost(10,3). cost(14,3).
cost(0,1). cost(1,1). cost(3,1). cost(4,1). cost(5,1). cost(6,1). cost(7,1). cost(8,1). cost(9,1). cost(11,1). cost(12,1). cost(13,1). cost(15,1).

% Standard edges
standard_edge(1,3). standard_edge(1,4). standard_edge(2,6). standard_edge(3,7). standard_edge(4,8). standard_edge(5,11). standard_edge(6,7). standard_edge(7,12). standard_edge(8,12). standard_edge(11,13). standard_edge(12,13). standard_edge(13,14).

% Heavy edges
heavy_edge(0,5). heavy_edge(9,10). heavy_edge(14,15).

% Master vertices
master(0). master(15).

% Antagonistic pairs
antagonistic(1,2). antagonistic(8,9).

% Choice of selected vertices
{ selected(V) } :- vertex(V).

% Standard edge coverage
:- standard_edge(U,V), not selected(U), not selected(V).

% Heavy edge coverage constraints
:- heavy_edge(U,V), not selected(U), not selected(V).
:- heavy_edge(U,V), selected(U), not selected(V), not master(U).
:- heavy_edge(U,V), selected(V), not selected(U), not master(V).

% Antagonistic pairs
:- antagonistic(U,V), selected(U), selected(V).

% Compute total cost
total_cost(C) :- C = #sum{ C1,V : selected(V), cost(V,C1) }.

% Optimization
#minimize { C,V : selected(V), cost(V,C) }.

% Show selected vertices and total cost
#show selected/1.
#show total_cost/1.