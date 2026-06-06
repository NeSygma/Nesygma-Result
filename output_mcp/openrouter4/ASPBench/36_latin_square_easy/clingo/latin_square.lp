% Latin square 5x5
% Define rows, columns, and numbers
row(1..5).
col(1..5).
num(1..5).

% Each cell gets exactly one number
1 { cell(R, C, N) : num(N) } 1 :- row(R), col(C).

% Fixed given values
cell(1,1,1).
cell(2,3,3).
cell(3,4,4).
cell(4,5,5).
cell(5,2,2).

% Each row must contain each number exactly once
:- row(R), num(N), not 1 { cell(R, C, N) : col(C) } 1.

% Each column must contain each number exactly once
:- col(C), num(N), not 1 { cell(R, C, N) : row(R) } 1.

% Show solution
#show cell/3.