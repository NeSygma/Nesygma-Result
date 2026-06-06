% Vertices
vertex(1). vertex(2). vertex(3). vertex(4). vertex(5). vertex(6). vertex(7). vertex(8). vertex(9). vertex(10). vertex(11). vertex(12). vertex(13). vertex(14). vertex(15). vertex(16). vertex(17). vertex(18).

% Edges (undirected, both directions)
edge(1,2). edge(2,1).
edge(1,4). edge(4,1).
edge(1,5). edge(5,1).
edge(2,4). edge(4,2).
edge(2,5). edge(5,2).
edge(3,4). edge(4,3).
edge(3,9). edge(9,3).
edge(4,5). edge(5,4).
edge(4,18). edge(18,4).
edge(6,7). edge(7,6).
edge(6,9). edge(9,6).
edge(6,10). edge(10,6).
edge(7,9). edge(9,7).
edge(8,9). edge(9,8).
edge(8,14). edge(14,8).
edge(9,10). edge(10,9).
edge(11,12). edge(12,11).
edge(11,14). edge(14,11).
edge(12,14). edge(14,12).
edge(13,14). edge(14,13).
edge(13,17). edge(17,13).
edge(15,16). edge(16,15).
edge(15,17). edge(17,15).
edge(16,17). edge(17,16).
edge(17,18). edge(18,17).

% Vertex types
% Critical
 type(1,c). type(5,c). type(10,c). type(15,c).
% Standard
 type(2,s). type(6,s). type(7,s). type(11,s). type(12,s). type(16,s).
% Resilient
 type(3,r). type(8,r). type(13,r). type(18,r).

% Vertex costs
cost(4,2). cost(9,2).
cost(14,3). cost(17,3).
cost(1,5). cost(2,5). cost(3,5). cost(5,5). cost(6,5). cost(7,5). cost(8,5).
cost(10,8). cost(11,8). cost(12,8). cost(13,8). cost(15,8). cost(16,8). cost(18,8).

% Choice of dominating set
{ selected(V) } :- vertex(V).

% Independent set constraint: no two adjacent vertices selected
:- selected(U), selected(V), edge(U,V).

% Domination constraints
% Critical and Standard: at least one neighbor selected if not selected
:- not selected(V), type(V,c), #count{N : edge(N,V), selected(N)} < 1.
:- not selected(V), type(V,s), #count{N : edge(N,V), selected(N)} < 1.
% Resilient: at least two neighbors selected if not selected
:- not selected(V), type(V,r), #count{N : edge(N,V), selected(N)} < 2.

% Objective: minimize total cost
#minimize { C : selected(V), cost(V,C) }.

% Compute total cost for display
total_cost(C) :- C = #sum { C1,V : selected(V), cost(V,C1) }.

#show selected/1.
#show total_cost/1.