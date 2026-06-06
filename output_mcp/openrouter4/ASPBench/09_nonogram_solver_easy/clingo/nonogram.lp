% Domain
row(1..5).
col(1..5).

% Row clues: row(R, clue_index, length)
row_clue(1, 1, 2).
row_clue(2, 1, 1).
row_clue(3, 1, 3).
row_clue(4, 1, 1).
row_clue(4, 2, 1).
row_clue(5, 1, 2).

% Column clues: col(C, clue_index, length)
col_clue(1, 1, 1).
col_clue(1, 2, 1).
col_clue(2, 1, 1).
col_clue(2, 2, 3).
col_clue(3, 1, 2).
col_clue(4, 1, 1).
col_clue(5, 1, 1).

% --- Row blocks ---
% Possible start columns for each row clue
possible_start_row(R, I, S) :- row_clue(R, I, L), col(S), S <= 5 - L + 1.

% Each clue picks exactly one start position
{ row_start(R, I, S) : possible_start_row(R, I, S) } 1 :- row_clue(R, I, _).

% Ordering and separation: later clues must start strictly after earlier clue's block
:- row_clue(R, I1, L1), row_clue(R, I2, L2), I1 < I2,
   row_start(R, I1, S1), row_start(R, I2, S2),
   S2 <= S1 + L1.

% Black cells derived from row blocks
black_row(R, C) :- row_start(R, I, S), row_clue(R, I, L), col(C),
                   S <= C, C < S + L.

% --- Column blocks ---
possible_start_col(C, J, S) :- col_clue(C, J, L), row(S), S <= 5 - L + 1.

{ col_start(C, J, S) : possible_start_col(C, J, S) } 1 :- col_clue(C, J, _).

:- col_clue(C, J1, L1), col_clue(C, J2, L2), J1 < J2,
   col_start(C, J1, S1), col_start(C, J2, S2),
   S2 <= S1 + L1.

black_col(C, R) :- col_start(C, J, S), col_clue(C, J, L), row(R),
                   S <= R, R < S + L.

% --- Consistency between row and column ---
% A cell is black if both row and column blocks say so
black(R, C) :- black_row(R, C), black_col(C, R).

% If one perspective says black, the other must too
:- black_row(R, C), not black_col(C, R).
:- black_col(C, R), not black_row(R, C).

% Show results
#show black/2.