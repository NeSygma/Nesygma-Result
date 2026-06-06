% Define the grid size
row(1..5).
col(1..5).
value(1..5).

% Pre-filled cells (given constraints)
cell(1,1,1).
cell(2,3,3).
cell(3,4,4).
cell(4,5,5).
cell(5,2,2).

% All cells must have exactly one value
{ cell(R,C,V) : value(V) } = 1 :- row(R), col(C).

% Each row must contain each value exactly once
:- row(R), value(V), #count{ C : cell(R,C,V) } != 1.

% Each column must contain each value exactly once
:- col(C), value(V), #count{ R : cell(R,C,V) } != 1.

% Show the solution
#show cell/3.