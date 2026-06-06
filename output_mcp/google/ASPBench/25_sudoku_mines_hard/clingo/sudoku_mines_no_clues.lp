% --- Domain ---
row(0..8).
col(0..8).
val(1..9).

% --- Mine-Count Clue Locations ---
mine_count_clue(0, 1).
mine_count_clue(3, 1).
mine_count_clue(5, 7).

% --- Sudoku Rules ---
1 { grid(R, C, V) : val(V) } 1 :- row(R), col(C).

:- grid(R, C1, V), grid(R, C2, V), C1 != C2.
:- grid(R1, C, V), grid(R2, C, V), R1 != R2.
:- grid(R1, C1, V), grid(R2, C2, V), R1/3 == R2/3, C1/3 == C2/3, (R1, C1) != (R2, C2).

% --- Mine Definition ---
mine(R, C) :- grid(R, C, V), V \ 2 == 0.

% --- Neighbor Definition ---
neighbor(R, C, NR, NC) :- row(R), col(C), row(NR), col(NC),
                          abs(R-NR) <= 1, abs(C-NC) <= 1,
                          (R, C) != (NR, NC).

% --- Mine-Count Clue Constraints ---
mine_count(R, C, N) :- mine_count_clue(R, C), N = #count { NR, NC : neighbor(R, C, NR, NC), mine(NR, NC) }.

:- mine_count_clue(R, C), grid(R, C, V), mine_count(R, C, N), V != N.

% --- Output ---
#show grid/3.
#show mine/2.
#show mine_count/3.