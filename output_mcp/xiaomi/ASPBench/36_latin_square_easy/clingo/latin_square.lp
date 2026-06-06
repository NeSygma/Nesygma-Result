% Latin Square 5x5 Solver

% Domain definitions
row(1..5).
col(1..5).
num(1..5).

% Given fixed values
fixed(1,1,1).
fixed(2,3,3).
fixed(3,4,4).
fixed(4,5,5).
fixed(5,2,2).

% For cells that are not fixed, we choose a number
{ grid(R,C,N) : num(N) } 1 :- row(R), col(C), not fixed(R,C,_).

% For fixed cells, the value is determined
grid(R,C,N) :- fixed(R,C,N).

% Each row must contain each number exactly once
:- row(R), num(N), not 1 { grid(R,C,N) : col(C) } 1.

% Each column must contain each number exactly once
:- col(C), num(N), not 1 { grid(R,C,N) : row(R) } 1.

% Each cell must have exactly one number (already handled by choice rule, but explicit)
:- row(R), col(C), not 1 { grid(R,C,N) : num(N) } 1.

% Show the solution
#show grid/3.