% Domain definitions
row(1..5).
col(1..5).
val(1..5).

% Fixed values
fixed(1, 1, 1).
fixed(2, 3, 3).
fixed(3, 4, 4).
fixed(4, 5, 5).
fixed(5, 2, 2).

% Each cell must have exactly one value
{ grid(R, C, V) : val(V) } = 1 :- row(R), col(C).

% Each row must contain each number exactly once
:- row(R), val(V), #count { C : grid(R, C, V) } != 1.

% Each column must contain each number exactly once
:- col(C), val(V), #count { R : grid(R, C, V) } != 1.

% Fixed values must be respected
:- fixed(R, C, V), not grid(R, C, V).

% Solved indicator
solved :- #count { R, C, V : grid(R, C, V) } = 25.

#show grid/3.
#show solved.