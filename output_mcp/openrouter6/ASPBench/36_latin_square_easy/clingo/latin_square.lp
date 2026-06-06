% Latin Square 5x5 Problem
% Domain declarations
row(1..5).
col(1..5).
num(1..5).

% Fixed cells from the problem
fixed(1,1,1).
fixed(2,3,3).
fixed(3,4,4).
fixed(4,5,5).
fixed(5,2,2).

% Choice rule: each cell gets exactly one number
1 { grid(R, C, N) : num(N) } 1 :- row(R), col(C).

% Fixed cells must have their assigned values
grid(R, C, N) :- fixed(R, C, N).

% Row uniqueness: each row contains each number exactly once
1 { grid(R, C, N) : col(C) } 1 :- row(R), num(N).

% Column uniqueness: each column contains each number exactly once
1 { grid(R, C, N) : row(R) } 1 :- col(C), num(N).

% Show the solved grid
#show grid/3.
#show solved.
solved :- grid(1,1,1), grid(2,3,3), grid(3,4,4), grid(4,5,5), grid(5,2,2).