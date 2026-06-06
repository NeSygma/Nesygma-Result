% ===== DOMAINS =====
row(0..8).
col(0..8).
val(1..9).

% ===== PRE-FILLED CLUES (can be overridden) =====
clue(0,0,5). clue(0,4,7). clue(0,8,2).
clue(4,0,4). clue(4,4,5). clue(4,8,1).
clue(8,0,3). clue(8,4,8). clue(8,8,9).

% ===== MINE-COUNT CLUE LOCATIONS =====
mine_clue(0,1).
mine_clue(3,1).
mine_clue(5,7).

% ===== ASSIGN EXACTLY ONE VALUE PER CELL =====
1 { cell(R,C,V) : val(V) } 1 :- row(R), col(C).

% ===== SUDOKU CONSTRAINTS =====
% Each row contains each value exactly once
1 { cell(R,C,V) : col(C) } 1 :- row(R), val(V).
% Each column contains each value exactly once
1 { cell(R,C,V) : row(R) } 1 :- col(C), val(V).
% Each 3x3 box contains each value exactly once
box_row(BR, 3*BR..3*BR+2) :- row(BR), BR < 3.
box_col(BC, 3*BC..3*BC+2) :- col(BC), BC < 3.
1 { cell(R,C,V) : row(R), col(C), R >= 3*BR, R <= 3*BR+2, C >= 3*BC, C <= 3*BC+2 } 1 :- row(BR), BR < 3, col(BC), BC < 3, val(V).

% ===== MINE DEFINITION =====
% A cell is a mine iff its value is even (2,4,6,8)
mine(R,C) :- cell(R,C,V), V = 2.
mine(R,C) :- cell(R,C,V), V = 4.
mine(R,C) :- cell(R,C,V), V = 6.
mine(R,C) :- cell(R,C,V), V = 8.

% ===== NEIGHBOR DEFINITION =====
% 8-connected neighbors (orthogonal + diagonal)
neighbor(R1,C1,R2,C2) :- row(R1), col(C1), row(R2), col(C2),
                          |R1-R2| <= 1, |C1-C2| <= 1, (R1,C1) != (R2,C2).

% ===== MINE COUNT FOR MINE-CLUE CELLS =====
mine_count(R,C,N) :- mine_clue(R,C), N = #count{ R2,C2 : neighbor(R,C,R2,C2), mine(R2,C2) }.

% ===== MINE-COUNT CONSTRAINT (HIGHEST PRIORITY) =====
% The value in a mine-count clue cell must equal the count of neighboring mines
:- mine_clue(R,C), cell(R,C,V), mine_count(R,C,N), V != N.

% ===== OUTPUT =====
#show cell/3.
#show mine/2.