% Domains
row(1..5).
col(1..5).
number(1..5).

% Given values (fixed cells)
given(1, 1, 1).
given(2, 3, 3).
given(3, 4, 4).
given(4, 5, 5).
given(5, 2, 2).

% Choice rule for empty cells
{ cell(R, C, N) : number(N) } = 1 :- row(R), col(C), not given(R, C, _).

% Enforce given values
cell(R, C, N) :- given(R, C, N).

% Each row must contain each number exactly once
:- row(R), number(N), { cell(R, C, N) : col(C) } != 1.

% Each column must contain each number exactly once
:- col(C), number(N), { cell(R, C, N) : row(R) } != 1.

% Ensure all cells are filled (no empty cells)
:- row(R), col(C), not cell(R, C, _).

% Show the solution
#show cell/3.