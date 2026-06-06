% Latin Square Solver for 5x5 grid

% Domain declarations
row(1..5).
col(1..5).
num(1..5).

% Fixed values from the problem
fixed(1,1,1).
fixed(2,3,3).
fixed(3,4,4).
fixed(4,5,5).
fixed(5,2,2).

% Choice rule for grid assignment
{ grid(R, C, N) } :- row(R), col(C), num(N).

% Fixed values must be assigned
grid(R, C, N) :- fixed(R, C, N).

% Each cell must have exactly one number
1 { grid(R, C, N) : num(N) } 1 :- row(R), col(C).

% Each row must contain each number exactly once
1 { grid(R, C, N) : col(C) } 1 :- row(R), num(N).

% Each column must contain each number exactly once
1 { grid(R, C, N) : row(R) } 1 :- col(C), num(N).

% Solution found if all cells are assigned
solved :- row(R), col(C), 1 = #count { N : grid(R, C, N) }.

% Show the solution
#show grid/3.
#show solved/0.