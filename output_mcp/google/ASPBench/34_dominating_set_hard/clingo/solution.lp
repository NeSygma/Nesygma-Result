% Graph definition
vertex(1..18).
edge(1,2). edge(1,4). edge(1,5). edge(2,4). edge(2,5). edge(3,4). edge(3,9). edge(4,5). edge(4,18).
edge(6,7). edge(6,9). edge(6,10). edge(7,9). edge(8,9). edge(8,14). edge(9,10). edge(11,12). edge(11,14).
edge(12,14). edge(13,14). edge(13,17). edge(15,16). edge(15,17). edge(16,17). edge(17,18).
edge(Y,X) :- edge(X,Y).

% Vertex types
type(1, c). type(5, c). type(10, c). type(15, c).
type(2, s). type(6, s). type(7, s). type(11, s). type(12, s). type(16, s).
type(3, r). type(8, r). type(13, r). type(18, r).
% Assuming 4, 9, 14, 17 are 's' (Standard)
type(4, s). type(9, s). type(14, s). type(17, s).

% Vertex costs
cost(1, 5). cost(2, 5). cost(3, 5). cost(4, 2). cost(5, 5). cost(6, 5). cost(7, 5). cost(8, 5). cost(9, 2).
cost(10, 8). cost(11, 8). cost(12, 8). cost(13, 8). cost(14, 3). cost(15, 8). cost(16, 8). cost(17, 3). cost(18, 8).

% Decision: Select vertices for the dominating set
{ in_set(V) } :- vertex(V).

% Constraint 1: Independent Set
:- in_set(U), in_set(V), edge(U, V).

% Domination logic
% A vertex is dominated if it is in the set OR it meets its type's requirement
is_dominated(V) :- in_set(V).
is_dominated(V) :- type(V, c), in_set(U), edge(V, U).
is_dominated(V) :- type(V, s), in_set(U), edge(V, U).
is_dominated(V) :- type(V, r), #count { U : in_set(U), edge(V, U) } >= 2.

% Constraint 5: All vertices must be dominated
:- vertex(V), not is_dominated(V).

% Objective: Minimize total cost
total_cost(C) :- C = #sum { Cost, V : in_set(V), cost(V, Cost) }.
#minimize { C : total_cost(C) }.

#show in_set/1.
#show total_cost/1.