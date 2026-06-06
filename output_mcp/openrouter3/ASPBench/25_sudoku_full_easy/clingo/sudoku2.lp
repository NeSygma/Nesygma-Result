% Sudoku Solver in ASP

% Domain declarations
row(1..9).
col(1..9).
digit(1..9).
box_row(1..3).
box_col(1..3).

% Cell positions
cell(R, C) :- row(R), col(C).

% Box definitions: each box covers 3 rows and 3 columns
% Box (BR, BC) contains rows (BR-1)*3+1 to BR*3 and columns (BC-1)*3+1 to BC*3
in_box(R, C, BR, BC) :-
    cell(R, C),
    box_row(BR),
    box_col(BC),
    R >= (BR-1)*3 + 1, R <= BR*3,
    C >= (BC-1)*3 + 1, C <= BC*3.

% Given clues from the puzzle
clue(1,1,5). clue(1,2,3). clue(1,5,7).
clue(2,1,6). clue(2,4,1). clue(2,5,9). clue(2,6,5).
clue(3,2,9). clue(3,3,8). clue(3,8,6).
clue(4,1,8). clue(4,5,6). clue(4,9,3).
clue(5,1,4). clue(5,4,8). clue(5,6,3). clue(5,9,1).
clue(6,1,7). clue(6,5,2). clue(6,9,6).
clue(7,2,6). clue(7,7,2). clue(7,8,8).
clue(8,4,4). clue(8,5,1). clue(8,6,9). clue(8,9,5).
clue(9,5,8). clue(9,7,7). clue(9,8,9). clue(9,9,9).

% Choice rule: each cell gets exactly one digit
{ value(R, C, D) : digit(D) } 1 :- cell(R, C).

% Constraint: clues must be preserved
:- clue(R, C, D), not value(R, C, D).

% Constraint: each row has all digits 1-9 exactly once
% For each row R and digit D, there must be exactly one column C where value(R,C,D) holds
:- row(R), digit(D), N = #count{C : value(R, C, D)}, N != 1.

% Constraint: each column has all digits 1-9 exactly once
% For each column C and digit D, there must be exactly one row R where value(R,C,D) holds
:- col(C), digit(D), N = #count{R : value(R, C, D)}, N != 1.

% Constraint: each 3x3 box has all digits 1-9 exactly once
% For each box (BR,BC) and digit D, there must be exactly one cell (R,C) in that box with value D
:- box_row(BR), box_col(BC), digit(D),
   N = #count{R, C : value(R, C, D), in_box(R, C, BR, BC)}, N != 1.

% Show the solution
#show value/3.