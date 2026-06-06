% --- Domain and Facts ---
% Cells
cell(0..8, 0..8).

% Values
val(1..9).

% Sudoku clues (pre-filled cells)
sudoku_clue(0,0,5). sudoku_clue(0,4,7). sudoku_clue(0,8,2).
sudoku_clue(4,0,4). sudoku_clue(4,4,5). sudoku_clue(4,8,1).
sudoku_clue(8,0,3). sudoku_clue(8,4,8). sudoku_clue(8,8,9).

% Mine-count clue locations
mine_clue(0,1). mine_clue(3,1). mine_clue(5,7).

% Even values
even(2). even(4). even(6). even(8).

% --- Choice Rule for Cell Values ---
{value(Row, Col, Val) : val(Val)} = 1 :- cell(Row, Col).

% --- Mine Definition ---
mine(Row, Col) :- value(Row, Col, Val), even(Val).

% --- Neighbor Definition ---
neighbor(R, C, NR, NC) :- cell(R, C), cell(NR, NC),
                          abs(R-NR) <= 1, abs(C-NC) <= 1,
                          (R, C) != (NR, NC).

% --- Mine-Count Clue Constraints ---
% For each mine-count clue cell, the value must equal the number of neighboring mines.
mine_count_clue_satisfied(R, C) :-
    mine_clue(R, C),
    value(R, C, N),
    N = #count { NRow, NCol : neighbor(R, C, NRow, NCol), mine(NRow, NCol) }.

% Ensure all mine-count clues are satisfied.
:- mine_clue(R, C), not mine_count_clue_satisfied(R, C).

% --- Sudoku Rules ---
% Each row must contain digits 1-9 exactly once.
:- row(R), val(V), not {value(R, C, V) : cell(R, C)} = 1.
row(0..8).

% Each column must contain digits 1-9 exactly once.
:- col(C), val(V), not {value(R, C, V) : cell(R, C)} = 1.
col(0..8).

% Each 3x3 box must contain digits 1-9 exactly once.
box(0,0,0,2). box(0,1,0,2). box(0,2,0,2).
box(1,0,3,5). box(1,1,3,5). box(1,2,3,5).
box(2,0,6,8). box(2,1,6,8). box(2,2,6,8).

:- box(BR, BC, ER, EC), val(V),
   not {value(R, C, V) : cell(R, C),
                     BR*3 <= R, R < (BR+1)*3,
                     BC*3 <= C, C < (BC+1)*3} = 1.

% --- Sudoku Clue Preservation ---
% If a Sudoku clue is not overridden by a mine-count clue, its value must remain unchanged.
sudoku_clue_preserved(R, C, Val) :-
    sudoku_clue(R, C, Val),
    value(R, C, Val),
    not mine_clue(R, C).

% All Sudoku clues are preserved if none are overridden.
sudoku_clues_preserved :- {sudoku_clue_preserved(R, C, Val) : sudoku_clue(R, C, Val)} = 9.

% --- Output ---
#show value/3.
#show mine/2.
#show sudoku_clues_preserved/0.
#show mine_clue_satisfied/0.

% Helper to check if mine clues are satisfied
mine_clue_satisfied :- mine_count_clue_satisfied(0,1), mine_count_clue_satisfied(3,1), mine_count_clue_satisfied(5,7).
#show mine_clue_satisfied/0.