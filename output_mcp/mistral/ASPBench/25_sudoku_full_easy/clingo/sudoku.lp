% Define the grid size
row(1..9). col(1..9). value(1..9).

% Define the 3x3 boxes
box(1..9).
box_of(R, C, 1) :- R = 1..3, C = 1..3.
box_of(R, C, 2) :- R = 1..3, C = 4..6.
box_of(R, C, 3) :- R = 1..3, C = 7..9.
box_of(R, C, 4) :- R = 4..6, C = 1..3.
box_of(R, C, 5) :- R = 4..6, C = 4..6.
box_of(R, C, 6) :- R = 4..6, C = 7..9.
box_of(R, C, 7) :- R = 7..9, C = 1..3.
box_of(R, C, 8) :- R = 7..9, C = 4..6.
box_of(R, C, 9) :- R = 7..9, C = 7..9.

% Given clues
clue(1,1,5). clue(1,2,3). clue(1,5,7).
clue(2,1,6). clue(2,4,1). clue(2,5,9). clue(2,6,5).
clue(3,2,9). clue(3,3,8). clue(3,7,6).
clue(4,1,8). clue(4,5,6). clue(4,9,3).
clue(5,1,4). clue(5,4,8). clue(5,6,3). clue(5,9,1).
clue(6,1,7). clue(6,5,2). clue(6,9,6).
clue(7,2,6). clue(7,7,2). clue(7,8,8).
clue(8,4,4). clue(8,5,1). clue(8,6,9). clue(8,9,5).
clue(9,5,8). clue(9,7,7). clue(9,9,9).

% A cell has a value
1 { cell(R, C, V) : value(V) } 1 :- row(R), col(C).

% Respect the clues
:- clue(R, C, V), not cell(R, C, V).
:- clue(R, C, V), cell(R, C, V2), V != V2.

% Each value appears at most once in each row
:- row(R), value(V), cell(R, C1, V), cell(R, C2, V), C1 < C2.

% Each value appears at most once in each column
:- col(C), value(V), cell(R1, C, V), cell(R2, C, V), R1 < R2.

% Each value appears at most once in each box
:- box(B), value(V), cell(R1, C1, V), cell(R2, C2, V), box_of(R1, C1, B), box_of(R2, C2, B), (R1, C1) < (R2, C2).

% Show the solution
#show cell/3.