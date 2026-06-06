% --- Graph and Vertex Data ---
vertex(1..18).

edge(1,2). edge(1,4). edge(1,5). edge(2,4). edge(2,5). edge(3,4).
edge(3,9). edge(4,5). edge(4,18). edge(6,7). edge(6,9). edge(6,10).
edge(7,9). edge(8,9). edge(8,14). edge(9,10). edge(11,12). edge(11,14).
edge(12,14). edge(13,14). edge(13,17). edge(15,16). edge(15,17).
edge(16,17). edge(17,18).

% Vertex types
type(1, c). type(5, c). type(10, c). type(15, c).
type(2, s). type(6, s). type(7, s). type(11, s). type(12, s). type(16, s).
type(3, r). type(8, r). type(13, r). type(18, r).

% Vertex costs
cost(1,5). cost(2,5). cost(3,5). cost(4,2). cost(5,5). cost(6,5). cost(7,5).
cost(8,5). cost(9,2). cost(10,8). cost(11,8). cost(12,8). cost(13,8).
cost(14,3). cost(15,8). cost(16,8). cost(17,3). cost(18,8).

% --- Selection and Domination ---
{ selected(V) : vertex(V) }.

% Independent set constraint
:- selected(V1), selected(V2), edge(V1, V2).

% Domination definitions
dominated_by_one(V) :- selected(U), edge(V, U).
dominated_by_two(V) :- selected(U1), selected(U2), U1 != U2, edge(V, U1), edge(V, U2).

% Critical and standard vertices must be dominated by at least one selected vertex if not selected
:- type(V, c), not selected(V), not dominated_by_one(V).
:- type(V, s), not selected(V), not dominated_by_one(V).

% Resilient vertices must be dominated by at least two distinct selected vertices if not selected
:- type(V, r), not selected(V), not dominated_by_two(V).

% --- Objective ---
total_cost(C) :- C = #sum { Cost : selected(V), cost(V, Cost) }.

% --- Output ---
#show selected/1.
#show total_cost/1.
#minimize { C, V : selected(V), cost(V, C) }.