% Define the grid size
row(0..8). col(0..8).

% Define the 3x3 boxes (0-indexed)
% Box B is defined for cells (R, C) where B = (R // 3) * 3 + (C // 3)
box(R, C, B) :-
    R = 0..2, C = 0..2, B = 0.
box(R, C, B) :-
    R = 0..2, C = 3..5, B = 1.
box(R, C, B) :-
    R = 0..2, C = 6..8, B = 2.
box(R, C, B) :-
    R = 3..5, C = 0..2, B = 3.
box(R, C, B) :-
    R = 3..5, C = 3..5, B = 4.
box(R, C, B) :-
    R = 3..5, C = 6..8, B = 5.
box(R, C, B) :-
    R = 6..8, C = 0..2, B = 6.
box(R, C, B) :-
    R = 6..8, C = 3..5, B = 7.
box(R, C, B) :-
    R = 6..8, C = 6..8, B = 8.

% Define neighbors for each cell (8 directions)
neighbor(R1, C1, R2, C2) :-
    R2 = R1 - 1, C2 = C1 - 1, row(R2), col(C2).
neighbor(R1, C1, R2, C2) :-
    R2 = R1 - 1, C2 = C1,     row(R2), col(C2).
neighbor(R1, C1, R2, C2) :-
    R2 = R1 - 1, C2 = C1 + 1, row(R2), col(C2).
neighbor(R1, C1, R2, C2) :-
    R2 = R1,     C2 = C1 - 1, row(R2), col(C2).
neighbor(R1, C1, R2, C2) :-
    R2 = R1,     C2 = C1 + 1, row(R2), col(C2).
neighbor(R1, C1, R2, C2) :-
    R2 = R1 + 1, C2 = C1 - 1, row(R2), col(C2).
neighbor(R1, C1, R2, C2) :-
    R2 = R1 + 1, C2 = C1,     row(R2), col(C2).
neighbor(R1, C1, R2, C2) :-
    R2 = R1 + 1, C2 = C1 + 1, row(R2), col(C2).

% Original Sudoku clues (can be overridden by mine-count constraints)
sudoku_clue(0,0,5).
sudoku_clue(0,4,7).
sudoku_clue(0,8,2).
sudoku_clue(4,0,4).
sudoku_clue(4,4,5).
sudoku_clue(4,8,1).
sudoku_clue(8,0,3).
sudoku_clue(8,4,8).
sudoku_clue(8,8,9).

% Mine-count clue locations
mine_count_clue(0,1).
mine_count_clue(3,1).
mine_count_clue(5,7).

% Choice rule for cell values (1-9)
1 { cell(R, C, V) : value(V) } 1 :- row(R), col(C).

value(1..9).

% Define mines: a cell is a mine if its value is even
mine(R, C) :- cell(R, C, V), V mod 2 = 0.

% For mine-count clue cells, the cell value must equal the number of neighboring mines
:- mine_count_clue(R, C),
   cell(R, C, V),
   #count { R2, C2 : neighbor(R, C, R2, C2), mine(R2, C2) } != V.

% Sudoku rules: each row must contain digits 1-9 exactly once
:- row(R), value(V), not cell(R, _, V).
:- row(R), value(V), #count { C : cell(R, C, V) } > 1.

% Sudoku rules: each column must contain digits 1-9 exactly once
:- col(C), value(V), not cell(_, C, V).
:- col(C), value(V), #count { R : cell(R, C, V) } > 1.

% Sudoku rules: each 3x3 box must contain digits 1-9 exactly once
:- box(R, C, B), value(V), not cell(R, C, V).
:- box(R, C, B), value(V), #count { R2, C2 : box(R2, C2, B), cell(R2, C2, V) } > 1.

% Helper to check if a cell is a mine-count clue
is_mine_count_clue(R, C) :- mine_count_clue(R, C).

% Determine if sudoku clues were preserved (if a sudoku clue cell is changed, it's not preserved)
clue_preserved(R, C) :-
    sudoku_clue(R, C, V),
    cell(R, C, V),
    not is_mine_count_clue(R, C).

% Sudoku clues are preserved if all original clues remain unchanged
all_sudoku_clues_preserved :- 
    sudoku_clue(R, C, V),
    clue_preserved(R, C).

% Mine-count clues are satisfied if the constraints are met (already enforced above)
all_mine_count_clues_satisfied :- 
    mine_count_clue(R, C),
    cell(R, C, V),
    #count { R2, C2 : neighbor(R, C, R2, C2), mine(R2, C2) } = V.

% Objective atoms to show
#show cell/3.
#show all_sudoku_clues_preserved.
#show all_mine_count_clues_satisfied.

% Additional atoms for debugging
#show mine/2.
#show is_mine_count_clue/2.