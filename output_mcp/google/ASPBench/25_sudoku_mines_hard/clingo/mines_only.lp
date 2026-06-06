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
mine_count(R, C, N) :- mine_count_clue(R, C), N = #count { NR, NC : neighbor(R, C, NR, NC), mine(NR, NC) }.

:- mine_count_clue(R, C), grid(R, C, V), mine_count(R, C, N), V != N.

% --- Output ---
#show grid/3.
#show mine/2.
#show mine_count/3.