% --- Domain ---
row(0..8).
col(0..8).
val(1..9).

% --- Mine-Count Clue Locations ---
mine_count_clue(0, 1).
mine_count_clue(3, 1).
mine_count_clue(5, 7).

% --- Grid ---
1 { grid(R, C, V) : val(V) } 1 :- row(R), col(C).

% --- Mine Definition ---
mine(R, C) :- grid(R, C, V), V \ 2 == 0.

% --- Neighbor Definition ---
neighbor(R, C, NR, NC) :- row(R), col(C), row(NR), col(NC),
                          abs(R-NR) <= 1, abs(C-NC) <= 1,
                          (R, C) != (NR, NC).

% --- Mine-Count Clue Constraints ---
% Let's check if the clue cell itself can be a mine.
% If the clue cell is a mine, it is even.
% If the clue cell is not a mine, it is odd.
% The clue value must be between 0 and 8.
% The clue value must be odd if it's not a mine, and even if it's a mine.
% Wait, the clue value is the number of neighbors that are mines.
% If the clue cell is a mine, it is even. So the number of neighbors must be even.
% If the clue cell is not a mine, it is odd. So the number of neighbors must be odd.

mine_count(R, C, N) :- mine_count_clue(R, C), N = #count { NR, NC : neighbor(R, C, NR, NC), mine(NR, NC) }.

% Constraint: The value in the clue cell MUST be the count of neighboring mines.
:- mine_count_clue(R, C), grid(R, C, V), mine_count(R, C, N), V != N.

% --- Sudoku Rules ---
:- row(R), not 1 { grid(R, C, V) : col(C) } 9, val(V).
:- col(C), not 1 { grid(R, C, V) : row(R) } 9, val(V).
:- row(R1), col(C1), row(R2), col(C2), (R1, C1) != (R2, C2),
   R1/3 == R2/3, C1/3 == C2/3, grid(R1, C1, V), grid(R2, C2, V).

% --- Sudoku Clues (Hints) ---
% (0,0): 5, (0,4): 7, (0,8): 2
% (4,0): 4, (4,4): 5, (4,8): 1
% (8,0): 3, (8,4): 8, (8,8): 9
% These are hints, but mine-count clues take priority.
% Let's see if we can satisfy the mine-count clues first.
% If we can't, then the problem is indeed unsatisfiable.

#show grid/3.
#show mine/2.
#show mine_count/3.