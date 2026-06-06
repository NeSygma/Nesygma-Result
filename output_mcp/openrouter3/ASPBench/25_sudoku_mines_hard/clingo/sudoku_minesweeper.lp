% Sudoku Minesweeper Hybrid Problem

% Domain declarations
row(0..8).
col(0..8).
value(1..9).
even_value(2;4;6;8).

% Original Sudoku clues (pre-filled cells)
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

% Box mapping (3x3 boxes numbered 0-8)
% Box 0: rows 0-2, cols 0-2; Box 1: rows 0-2, cols 3-5; etc.
box(R, C, 0) :- row(R), col(C), R < 3, C < 3.
box(R, C, 1) :- row(R), col(C), R < 3, C >= 3, C < 6.
box(R, C, 2) :- row(R), col(C), R < 3, C >= 6.
box(R, C, 3) :- row(R), col(C), R >= 3, R < 6, C < 3.
box(R, C, 4) :- row(R), col(C), R >= 3, R < 6, C >= 3, C < 6.
box(R, C, 5) :- row(R), col(C), R >= 3, R < 6, C >= 6.
box(R, C, 6) :- row(R), col(C), R >= 6, C < 3.
box(R, C, 7) :- row(R), col(C), R >= 6, C >= 3, C < 6.
box(R, C, 8) :- row(R), col(C), R >= 6, C >= 6.

% Neighbor relationships (8 neighbors: orthogonal and diagonal)
neighbor(R, C, R-1, C-1) :- row(R), col(C), R > 0, C > 0.
neighbor(R, C, R-1, C)   :- row(R), col(C), R > 0.
neighbor(R, C, R-1, C+1) :- row(R), col(C), R > 0, C < 8.
neighbor(R, C, R, C-1)   :- row(R), col(C), C > 0.
neighbor(R, C, R, C+1)   :- row(R), col(C), C < 8.
neighbor(R, C, R+1, C-1) :- row(R), col(C), R < 8, C > 0.
neighbor(R, C, R+1, C)   :- row(R), col(C), R < 8.
neighbor(R, C, R+1, C+1) :- row(R), col(C), R < 8, C < 8.

% Main grid assignment - each cell gets exactly one value
1 { grid(R, C, V) : value(V) } 1 :- row(R), col(C).

% Mine definition: cell is mine iff its value is even
mine(R, C) :- grid(R, C, V), even_value(V).

% Standard Sudoku constraints
% Each row must have digits 1-9 exactly once
1 { grid(R, C, V) : col(C) } 1 :- row(R), value(V).
% Each column must have digits 1-9 exactly once  
1 { grid(R, C, V) : row(R) } 1 :- col(C), value(V).
% Each 3x3 box must have digits 1-9 exactly once
1 { grid(R, C, V) : box(R, C, B) } 1 :- B = 0..8, value(V).

% Mine-count clue constraint: value equals number of neighboring mines
% For each mine-count clue cell, count its neighboring mines
mine_count(R, C, N) :- 
    mine_count_clue(R, C),
    N = #count { R2, C2 : neighbor(R, C, R2, C2), mine(R2, C2) }.

% The mine-count clue cell's value must equal the mine count
:- mine_count_clue(R, C), grid(R, C, V), mine_count(R, C, N), V != N.

% Sudoku clues constraint: original clues should be preserved if possible
% But mine-count clues have higher priority, so we allow changes
% We'll track whether clues are preserved
sudoku_clues_preserved :- 
    sudoku_clue(R, C, V), grid(R, C, V).

% If any clue is violated, sudoku_clues_preserved is false
:- sudoku_clue(R, C, V), grid(R, C, V2), V != V2.

% Show the solution
solution_exists.
#show grid/3.
#show mine/2.
#show solution_exists.
#show sudoku_clues_preserved.
#show mine_clues_satisfied.

% Define mine_clues_satisfied based on whether all mine-count clues are correct
mine_clues_satisfied :- 
    mine_count_clue(R, C), 
    grid(R, C, V), 
    mine_count(R, C, V).

% If any mine-count clue is wrong, mine_clues_satisfied is false
:- mine_count_clue(R, C), grid(R, C, V), mine_count(R, C, N), V != N.