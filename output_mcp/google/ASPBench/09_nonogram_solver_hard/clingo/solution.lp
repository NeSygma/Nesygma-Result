% Grid size
#const n = 24.

% Palette: 0=white, 1=red, 2=green, 3=blue
color(0; 1; 2; 3).

% Grid definition
{ grid(R, C, Color) : color(Color) } = 1 :- R = 0..n-1, C = 0..n-1.

% --- Clues ---
% Row clues
row_clue(0, 0, 1, 10). row_clue(0, 1, 2, 4). row_clue(0, 2, 1, 10).
row_clue(1, 0, 1, 10). row_clue(1, 1, 2, 4). row_clue(1, 2, 1, 10).
row_clue(2, 0, 1, 2). row_clue(2, 1, 2, 4). row_clue(2, 2, 1, 2).
row_clue(3, 0, 1, 2). row_clue(3, 1, 2, 4). row_clue(3, 2, 1, 2).
row_clue(4, 0, 1, 2). row_clue(4, 1, 2, 4). row_clue(4, 2, 1, 2).
row_clue(5, 0, 1, 2). row_clue(5, 1, 2, 4). row_clue(5, 2, 1, 2).
row_clue(6, 0, 1, 2). row_clue(6, 1, 2, 4). row_clue(6, 2, 1, 2).
row_clue(7, 0, 1, 2). row_clue(7, 1, 2, 4). row_clue(7, 2, 1, 2).
row_clue(8, 0, 1, 2). row_clue(8, 1, 3, 8). row_clue(8, 2, 1, 2).
row_clue(9, 0, 1, 2). row_clue(9, 1, 3, 8). row_clue(9, 2, 1, 2).
row_clue(10, 0, 1, 2). row_clue(10, 1, 2, 6). row_clue(10, 2, 3, 8). row_clue(10, 3, 2, 6). row_clue(10, 4, 1, 2).
row_clue(11, 0, 1, 2). row_clue(11, 1, 2, 6). row_clue(11, 2, 3, 8). row_clue(11, 3, 2, 6). row_clue(11, 4, 1, 2).
row_clue(12, 0, 1, 2). row_clue(12, 1, 2, 6). row_clue(12, 2, 3, 8). row_clue(12, 3, 2, 6). row_clue(12, 4, 1, 2).
row_clue(13, 0, 1, 2). row_clue(13, 1, 2, 6). row_clue(13, 2, 3, 8). row_clue(13, 3, 2, 6). row_clue(13, 4, 1, 2).
row_clue(14, 0, 1, 2). row_clue(14, 1, 3, 8). row_clue(14, 2, 1, 2).
row_clue(15, 0, 1, 2). row_clue(15, 1, 3, 8). row_clue(15, 2, 1, 2).
row_clue(16, 0, 1, 2). row_clue(16, 1, 2, 4). row_clue(16, 2, 1, 2).
row_clue(17, 0, 1, 2). row_clue(17, 1, 2, 4). row_clue(17, 2, 1, 2).
row_clue(18, 0, 1, 2). row_clue(18, 1, 2, 4). row_clue(18, 2, 1, 2).
row_clue(19, 0, 1, 2). row_clue(19, 1, 2, 4). row_clue(19, 2, 1, 2).
row_clue(20, 0, 1, 2). row_clue(20, 1, 2, 4). row_clue(20, 2, 1, 2).
row_clue(21, 0, 1, 2). row_clue(21, 1, 2, 4). row_clue(21, 2, 1, 2).
row_clue(22, 0, 1, 10). row_clue(22, 1, 2, 4). row_clue(22, 2, 1, 10).
row_clue(23, 0, 1, 10). row_clue(23, 1, 2, 4). row_clue(23, 2, 1, 10).

% Column clues
col_clue(0, 0, 1, 24).
col_clue(1, 0, 1, 24).
col_clue(2, 0, 1, 2). col_clue(2, 1, 2, 4). col_clue(2, 2, 1, 2).
col_clue(3, 0, 1, 2). col_clue(3, 1, 2, 4). col_clue(3, 2, 1, 2).
col_clue(4, 0, 1, 2). col_clue(4, 1, 2, 4). col_clue(4, 2, 1, 2).
col_clue(5, 0, 1, 2). col_clue(5, 1, 2, 4). col_clue(5, 2, 1, 2).
col_clue(6, 0, 1, 2). col_clue(6, 1, 2, 4). col_clue(6, 2, 1, 2).
col_clue(7, 0, 1, 2). col_clue(7, 1, 2, 4). col_clue(7, 2, 1, 2).
col_clue(8, 0, 1, 2). col_clue(8, 1, 3, 8). col_clue(8, 2, 1, 2).
col_clue(9, 0, 1, 2). col_clue(9, 1, 3, 8). col_clue(9, 2, 1, 2).
col_clue(10, 0, 2, 8). col_clue(10, 1, 3, 8). col_clue(10, 2, 2, 8).
col_clue(11, 0, 2, 8). col_clue(11, 1, 3, 8). col_clue(11, 2, 2, 8).
col_clue(12, 0, 2, 8). col_clue(12, 1, 3, 8). col_clue(12, 2, 2, 8).
col_clue(13, 0, 2, 8). col_clue(13, 1, 3, 8). col_clue(13, 2, 2, 8).
col_clue(14, 0, 1, 2). col_clue(14, 1, 3, 8). col_clue(14, 2, 1, 2).
col_clue(15, 0, 1, 2). col_clue(15, 1, 3, 8). col_clue(15, 2, 1, 2).
col_clue(16, 0, 1, 2). col_clue(16, 1, 2, 4). col_clue(16, 2, 1, 2).
col_clue(17, 0, 1, 2). col_clue(17, 1, 2, 4). col_clue(17, 2, 1, 2).
col_clue(18, 0, 1, 2). col_clue(18, 1, 2, 4). col_clue(18, 2, 1, 2).
col_clue(19, 0, 1, 2). col_clue(19, 1, 2, 4). col_clue(19, 2, 1, 2).
col_clue(20, 0, 1, 2). col_clue(20, 1, 2, 4). col_clue(20, 2, 1, 2).
col_clue(21, 0, 1, 2). col_clue(21, 1, 2, 4). col_clue(21, 2, 1, 2).
col_clue(22, 0, 1, 24).
col_clue(23, 0, 1, 24).

% Main diagonal
main_diag_seq(0, 1). main_diag_seq(1, 1). main_diag_seq(2, 0). main_diag_seq(3, 0). main_diag_seq(4, 0). main_diag_seq(5, 0). main_diag_seq(6, 0). main_diag_seq(7, 0).
main_diag_seq(8, 3). main_diag_seq(9, 3). main_diag_seq(10, 3). main_diag_seq(11, 3). main_diag_seq(12, 3). main_diag_seq(13, 3). main_diag_seq(14, 3). main_diag_seq(15, 3).
main_diag_seq(16, 0). main_diag_seq(17, 0). main_diag_seq(18, 0). main_diag_seq(19, 0). main_diag_seq(20, 0). main_diag_seq(21, 0). main_diag_seq(22, 1). main_diag_seq(23, 1).

% Anti-diagonal
anti_diag_seq(0, 1). anti_diag_seq(1, 1). anti_diag_seq(2, 0). anti_diag_seq(3, 0). anti_diag_seq(4, 0). anti_diag_seq(5, 0). anti_diag_seq(6, 0). anti_diag_seq(7, 0).
anti_diag_seq(8, 3). anti_diag_seq(9, 3). anti_diag_seq(10, 3). anti_diag_seq(11, 3). anti_diag_seq(12, 3). anti_diag_seq(13, 3). anti_diag_seq(14, 3). anti_diag_seq(15, 3).
anti_diag_seq(16, 0). anti_diag_seq(17, 0). anti_diag_seq(18, 0). anti_diag_seq(19, 0). anti_diag_seq(20, 0). anti_diag_seq(21, 0). anti_diag_seq(22, 1). anti_diag_seq(23, 1).

% Constraints
:- R = 0..n-1, C = 0..n-1, main_diag_seq(R, Color), R == C, grid(R, C, GColor), GColor != Color.
:- R = 0..n-1, C = 0..n-1, anti_diag_seq(R, Color), C == n-1-R, grid(R, C, GColor), GColor != Color.

% Define runs in a row
run_start(R, C, Color) :- grid(R, C, Color), Color > 0, (C == 0 ; grid(R, C-1, PrevColor), PrevColor != Color).
run_end(R, C, Color) :- grid(R, C, Color), Color > 0, (C == n-1 ; grid(R, C+1, NextColor), NextColor != Color).

% A run is defined by its start and end
run(R, Start, End, Color) :- run_start(R, Start, Color), run_end(R, End, Color), Start <= End,
                             not grid(R, Start-1, Color) : Start > 0,
                             not grid(R, End+1, Color) : End < n-1.

% Collect all runs in a row
row_run(R, I, Color, Length) :- run(R, Start, End, Color), Length = End - Start + 1,
                                I = #count { S, E : run(R, S, E, _), S < Start }.

% Check row clues
:- R = 0..n-1, row_clue(R, I, Color, Length), not row_run(R, I, Color, Length).
:- R = 0..n-1, row_run(R, I, Color, Length), not row_clue(R, I, Color, Length).

% Define runs in a column
run_col_start(R, C, Color) :- grid(R, C, Color), Color > 0, (R == 0 ; grid(R-1, C, PrevColor), PrevColor != Color).
run_col_end(R, C, Color) :- grid(R, C, Color), Color > 0, (R == n-1 ; grid(R+1, C, NextColor), NextColor != Color).

run_col(C, Start, End, Color) :- run_col_start(Start, C, Color), run_col_end(End, C, Color), Start <= End,
                                 not grid(Start-1, C, Color) : Start > 0,
                                 not grid(End+1, C, Color) : End < n-1.

% Collect all runs in a column
col_run(C, I, Color, Length) :- run_col(C, Start, End, Color), Length = End - Start + 1,
                                I = #count { S, E : run_col(C, S, E, _), S < Start }.

% Check column clues
:- C = 0..n-1, col_clue(C, I, Color, Length), not col_run(C, I, Color, Length).
:- C = 0..n-1, col_run(C, I, Color, Length), not col_clue(C, I, Color, Length).

#show grid/3.