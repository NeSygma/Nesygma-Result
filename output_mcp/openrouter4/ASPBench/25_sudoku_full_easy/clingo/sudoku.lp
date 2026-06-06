% Define the grid
row(1..9).
col(1..9).
digit(1..9).

% 3x3 box identification
box_id(R, C, B) :- row(R), col(C), B = ((R-1)/3)*3 + ((C-1)/3) + 1.

% Each cell gets exactly one digit
1 { cell(R, C, D) : digit(D) } 1 :- row(R), col(C).

% Row constraint
:- row(R), digit(D), not 1 = #count { C : cell(R, C, D) }.

% Column constraint
:- col(C), digit(D), not 1 = #count { R : cell(R, C, D) }.

% Box constraint
:- digit(D), B = 1..9, not 1 = #count { R, C : cell(R, C, D), box_id(R, C, B) }.

% Given clues
cell(1,1,5).  cell(1,2,3).  cell(1,5,7).
cell(2,1,6).  cell(2,4,1).  cell(2,5,9).  cell(2,6,5).
cell(3,2,9).  cell(3,3,8).  cell(3,8,6).
cell(4,1,8).  cell(4,5,6).  cell(4,9,3).
cell(5,1,4).  cell(5,4,8).  cell(5,6,3).  cell(5,9,1).
cell(6,1,7).  cell(6,5,2).  cell(6,9,6).
cell(7,2,6).  cell(7,7,2).  cell(7,8,8).
cell(8,4,4).  cell(8,5,1).  cell(8,6,9).  cell(8,9,5).
cell(9,5,8).  cell(9,8,7).  cell(9,9,9).

#show cell/3.