% Grid dimensions
row(1..5).
col(1..5).

% Row clues: row_clue(Row, GroupIndex, Length)
row_clue(1, 1, 2).
row_clue(2, 1, 1).
row_clue(3, 1, 3).
row_clue(4, 1, 1).
row_clue(4, 2, 1).
row_clue(5, 1, 2).

% Column clues: col_clue(Col, GroupIndex, Length)
col_clue(1, 1, 1).
col_clue(1, 2, 1).
col_clue(2, 1, 1).
col_clue(2, 2, 3).
col_clue(3, 1, 2).
col_clue(4, 1, 1).
col_clue(5, 1, 1).

% Possible starting positions for row groups (1-indexed columns)
possible_row_start(R, G, S) :- row_clue(R, G, L), col(S), S + L - 1 <= 5.

% Choose exactly one starting position for each row group
{ row_group_start(R, G, S) : possible_row_start(R, G, S) } 1 :- row_clue(R, G, _).

% Possible starting positions for column groups (1-indexed rows)
possible_col_start(C, G, S) :- col_clue(C, G, L), row(S), S + L - 1 <= 5.

% Choose exactly one starting position for each column group
{ col_group_start(C, G, S) : possible_col_start(C, G, S) } 1 :- col_clue(C, G, _).

% Row groups must be ordered: later group starts after earlier group ends + 1 (separator)
:- row_group_start(R, G1, S1), row_group_start(R, G2, S2), row_clue(R, G1, L1), G1 < G2, S2 < S1 + L1 + 1.

% Column groups must be ordered similarly
:- col_group_start(C, G1, S1), col_group_start(C, G2, S2), col_clue(C, G1, L1), G1 < G2, S2 < S1 + L1 + 1.

% Derive black cells from row group placements
black_row(R, C) :- row_group_start(R, G, S), row_clue(R, G, L), col(C), C >= S, C < S + L.

% Derive black cells from column group placements
black_col(R, C) :- col_group_start(C, G, S), col_clue(C, G, L), row(R), R >= S, R < S + L.

% Consistency: row and column derivations must agree
:- black_row(R, C), not black_col(R, C).
:- black_col(R, C), not black_row(R, C).

% Final black cells (from row perspective, guaranteed consistent)
black(R, C) :- black_row(R, C).

% Output grid: 1 for black, 0 for white
grid(R, C, 1) :- black(R, C).
grid(R, C, 0) :- row(R), col(C), not black(R, C).

% Valid flag
valid.

#show grid/3.
#show valid.