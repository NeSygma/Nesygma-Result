% Define the grid and digits.
row(1..9).
col(1..9).
digit(1..9).

% Define cells.
cell(X, Y) :- row(X), col(Y).

% Given clues (row, column, digit).
clue(1, 1, 5). clue(1, 2, 3). clue(1, 5, 7).
clue(2, 1, 6). clue(2, 4, 1). clue(2, 5, 9). clue(2, 6, 5).
clue(3, 2, 9). clue(3, 3, 8). clue(3, 8, 6).
clue(4, 1, 8). clue(4, 5, 6). clue(4, 9, 3).
clue(5, 1, 4). clue(5, 4, 8). clue(5, 6, 3). clue(5, 9, 1).
clue(6, 1, 7). clue(6, 5, 2). clue(6, 9, 6).
clue(7, 2, 6). clue(7, 8, 2). clue(7, 9, 8).
clue(8, 4, 4). clue(8, 5, 1). clue(8, 6, 9). clue(8, 9, 5).
clue(9, 5, 8). clue(9, 8, 7). clue(9, 9, 9).

% Assign digits to non-clue cells.
1 { value(X, Y, D) : digit(D) } 1 :- cell(X, Y), not clue(X, Y, _).

% Clue cells must have the given digit.
value(X, Y, D) :- clue(X, Y, D).

% Row constraint: Each digit must appear exactly once in each row.
:- row(X), digit(D), 2 { value(X, Y, D) : col(Y) }.

% Column constraint: Each digit must appear exactly once in each column.
:- col(Y), digit(D), 2 { value(X, Y, D) : row(X) }.

% Box constraint: Each digit must appear exactly once in each 3x3 box.
:- digit(D), box(BX, BY),
   2 { value(X, Y, D) : cell(X, Y), box_row(BX, X), box_col(BY, Y) }.

% Define 3x3 boxes.
box(1, 1). box(1, 2). box(1, 3).
box(2, 1). box(2, 2). box(2, 3).
box(3, 1). box(3, 2). box(3, 3).

box_row(1, X) :- X = 1..3.
box_row(2, X) :- X = 4..6.
box_row(3, X) :- X = 7..9.

box_col(1, Y) :- Y = 1..3.
box_col(2, Y) :- Y = 4..6.
box_col(3, Y) :- Y = 7..9.

% Show the solution.
#show value/3.