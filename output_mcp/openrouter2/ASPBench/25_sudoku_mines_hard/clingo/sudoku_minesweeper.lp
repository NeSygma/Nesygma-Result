% Domain facts
row(0..8).
col(0..8).
digit(1..9).
box(0,0). box(0,3). box(0,6).
box(3,0). box(3,3). box(3,6).
box(6,0). box(6,3). box(6,6).

% Sudoku clues
clue(0,0,5). clue(0,4,7). clue(0,8,2).
clue(4,0,4). clue(4,4,5). clue(4,8,1).
clue(8,0,3). clue(8,4,8). clue(8,8,9).

% Mine-count clue locations
mine_clue(0,1). mine_clue(3,1). mine_clue(5,7).

% Each cell gets exactly one digit
{ grid(R,C,D) : digit(D) } 1 :- row(R), col(C).

% Sudoku constraints
1 { grid(R,C,D) : col(C) } 1 :- row(R), digit(D).
1 { grid(R,C,D) : row(R) } 1 :- col(C), digit(D).

% Box cells
box_cell(BR,BC,R,C) :- box(BR,BC), row(R), col(C), R>=BR, R<BR+3, C>=BC, C<BC+3.
1 { grid(R,C,D) : box_cell(BR,BC,R,C) } 1 :- box(BR,BC), digit(D).

% Even digits define mines
even(R,C) :- grid(R,C,2).
even(R,C) :- grid(R,C,4).
even(R,C) :- grid(R,C,6).
even(R,C) :- grid(R,C,8).
mine(R,C) :- even(R,C).

% Neighbor relation
neighbor(R,C,R2,C2) :- row(R), col(C), row(R2), col(C2),
    R2>=R-1, R2<=R+1, C2>=C-1, C2<=C+1,
    (R2 != R ; C2 != C).

% Count mines around a cell
count_mines(R,C,N) :- row(R), col(C), N = #count{R2,C2 : neighbor(R,C,R2,C2), even(R2,C2)}.

% Mine-count clue satisfaction
satisfied(R,C) :- mine_clue(R,C), grid(R,C,V), count_mines(R,C,V).
:- mine_clue(R,C), not satisfied(R,C).

% Preserve Sudoku clues if unchanged
preserved(R,C) :- clue(R,C,V), grid(R,C,V).
preserved_all :- preserved(0,0), preserved(0,4), preserved(0,8),
                 preserved(4,0), preserved(4,4), preserved(4,8),
                 preserved(8,0), preserved(8,4), preserved(8,8).
sudoku_clues_preserved :- preserved_all.

% Sudoku validity flag
is_valid_sudoku.

% Mine clues satisfied flag
mine_clues_satisfied :- satisfied(0,1), satisfied(3,1), satisfied(5,7).

% Minimize lexicographically
#minimize { (R*9+C)*10 + D : grid(R,C,D) }.

% Show atoms
#show grid/3.
#show mine/2.
#show is_valid_sudoku.
#show sudoku_clues_preserved.
#show mine_clues_satisfied.