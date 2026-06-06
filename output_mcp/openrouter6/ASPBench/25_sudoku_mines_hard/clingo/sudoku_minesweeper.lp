% Sudoku-Minesweeper Hybrid Puzzle

% Domains
row(0..8).
col(0..8).
digit(1..9).

% Original Sudoku clues (hints) - these can be changed if mine-count constraints require it
original_clue(0,0,5).
original_clue(0,4,7).
original_clue(0,8,2).
original_clue(4,0,4).
original_clue(4,4,5).
original_clue(4,8,1).
original_clue(8,0,3).
original_clue(8,4,8).
original_clue(8,8,9).

% Mine-count clue locations
mine_count_cell(0,1).
mine_count_cell(3,1).
mine_count_cell(5,7).

% Grid assignment: exactly one digit per cell
1 { cell(R,C,D) : digit(D) } 1 :- row(R), col(C).

% Sudoku constraints: each row has each digit exactly once
:- row(R), digit(D), #count{ C : cell(R,C,D) } != 1.

% Sudoku constraints: each column has each digit exactly once  
:- col(C), digit(D), #count{ R : cell(R,C,D) } != 1.

% Sudoku constraints: each 3x3 box has each digit exactly once
% Box 0: rows 0-2, cols 0-2; Box 1: rows 0-2, cols 3-5; etc.
:- digit(D), 
   #count{ R,C : row(R), col(C), cell(R,C,D), R/3=0, C/3=0 } != 1.
:- digit(D), 
   #count{ R,C : row(R), col(C), cell(R,C,D), R/3=0, C/3=1 } != 1.
:- digit(D), 
   #count{ R,C : row(R), col(C), cell(R,C,D), R/3=0, C/3=2 } != 1.
:- digit(D), 
   #count{ R,C : row(R), col(C), cell(R,C,D), R/3=1, C/3=0 } != 1.
:- digit(D), 
   #count{ R,C : row(R), col(C), cell(R,C,D), R/3=1, C/3=1 } != 1.
:- digit(D), 
   #count{ R,C : row(R), col(C), cell(R,C,D), R/3=1, C/3=2 } != 1.
:- digit(D), 
   #count{ R,C : row(R), col(C), cell(R,C,D), R/3=2, C/3=0 } != 1.
:- digit(D), 
   #count{ R,C : row(R), col(C), cell(R,C,D), R/3=2, C/3=1 } != 1.
:- digit(D), 
   #count{ R,C : row(R), col(C), cell(R,C,D), R/3=2, C/3=2 } != 1.

% Mine definition: cell is mine if digit is even (2,4,6,8)
mine(R,C) :- cell(R,C,D), D = 2.
mine(R,C) :- cell(R,C,D), D = 4.
mine(R,C) :- cell(R,C,D), D = 6.
mine(R,C) :- cell(R,C,D), D = 8.

% Helper: neighbor count for any cell (8 neighbors: orthogonal + diagonal)
% For cell (R,C), neighbors are (R-1,C-1), (R-1,C), (R-1,C+1), (R,C-1), (R,C+1), (R+1,C-1), (R+1,C), (R+1,C+1)
neighbor(R,C,Rn,Cn) :- 
    row(R), col(C),
    row(Rn), col(Cn),
    Rn >= 0, Rn <= 8, Cn >= 0, Cn <= 8,
    Rn != R, Cn != C,
    Rn >= R-1, Rn <= R+1,
    Cn >= C-1, Cn <= C+1.

neighbor_count(R,C,N) :- 
    row(R), col(C),
    N = #count{ Rn,Cn : neighbor(R,C,Rn,Cn), mine(Rn,Cn) }.

% Mine-count constraints: the three specific cells must have value equal to neighbor mine count
:- mine_count_cell(R,C), cell(R,C,D), neighbor_count(R,C,N), D != N.

% Track if original clues are preserved
sudoku_clues_preserved :-
    #count{ R,C,D : original_clue(R,C,D), cell(R,C,D) } = 9.

% If not all clues preserved, then false (using choice rule)
{ sudoku_clues_preserved } :- not sudoku_clues_preserved.

% Mine clues satisfied (should always be true due to constraint above)
mine_clues_satisfied :-
    mine_count_cell(R,C),
    cell(R,C,D),
    neighbor_count(R,C,N),
    D = N.

% Show the grid
#show cell/3.
#show sudoku_clues_preserved/0.
#show mine_clues_satisfied/0.