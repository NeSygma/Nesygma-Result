% Define the grid dimensions
row(1..9).
col(1..9).
digit(1..9).

% Define 3x3 box membership
% Box number for each cell (row, col) -> box
box(R, C, B) :- row(R), col(C), B = ((R-1)/3)*3 + ((C-1)/3) + 1.

% Given clues (fixed cells)
clue(1,1,5). clue(1,2,3). clue(1,5,7).
clue(2,1,6). clue(2,4,1). clue(2,5,9). clue(2,6,5).
clue(3,2,9). clue(3,3,8). clue(3,8,6).
clue(4,1,8). clue(4,5,6). clue(4,9,3).
clue(5,1,4). clue(5,4,8). clue(5,6,3). clue(5,9,1).
clue(6,1,7). clue(6,5,2). clue(6,9,6).
clue(7,2,6). clue(7,7,2). clue(7,8,8).
clue(8,4,4). clue(8,5,1). clue(8,6,9). clue(8,9,5).
clue(9,5,8). clue(9,8,7). clue(9,9,9).

% A cell is a clue cell if it has a given value
clue_cell(R, C) :- clue(R, C, _).

% For non-clue cells, choose a digit
{ cell(R, C, D) : digit(D) } 1 :- row(R), col(C), not clue_cell(R, C).

% For clue cells, the value is fixed
cell(R, C, D) :- clue(R, C, D).

% Constraint 1: Each row must contain each digit exactly once
:- row(R), digit(D), #count{C : cell(R, C, D)} != 1.

% Constraint 2: Each column must contain each digit exactly once
:- col(C), digit(D), #count{R : cell(R, C, D)} != 1.

% Constraint 3: Each 3x3 box must contain each digit exactly once
:- box(R1, C1, B), digit(D), #count{R, C : box(R, C, B), cell(R, C, D)} != 1.

% Show the solution
#show cell/3.