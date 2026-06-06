% Grid size
size(24).

% Palette
color(0). color(1). color(2). color(3).

% Grid cells
1 { color(X, Y, C) : color(C) } 1 :- size(N), X = 1..N, Y = 1..N.

% Row run clues (row, run_index, color, length)
% Row 1: [(1,10), (2,4), (1,10)]
row_run(1, 1, 1, 10).
row_run(1, 2, 2, 4).
row_run(1, 3, 1, 10).

% Row 2: [(1,10), (2,4), (1,10)]
row_run(2, 1, 1, 10).
row_run(2, 2, 2, 4).
row_run(2, 3, 1, 10).

% Row 3: [(1,2), (2,4), (1,2)]
row_run(3, 1, 1, 2).
row_run(3, 2, 2, 4).
row_run(3, 3, 1, 2).

% Row 4: [(1,2), (2,4), (1,2)]
row_run(4, 1, 1, 2).
row_run(4, 2, 2, 4).
row_run(4, 3, 1, 2).

% Row 5: [(1,2), (2,4), (1,2)]
row_run(5, 1, 1, 2).
row_run(5, 2, 2, 4).
row_run(5, 3, 1, 2).

% Row 6: [(1,2), (2,4), (1,2)]
row_run(6, 1, 1, 2).
row_run(6, 2, 2, 4).
row_run(6, 3, 1, 2).

% Row 7: [(1,2), (2,4), (1,2)]
row_run(7, 1, 1, 2).
row_run(7, 2, 2, 4).
row_run(7, 3, 1, 2).

% Row 8: [(1,2), (2,4), (1,2)]
row_run(8, 1, 1, 2).
row_run(8, 2, 2, 4).
row_run(8, 3, 1, 2).

% Row 9: [(1,2), (3,8), (1,2)]
row_run(9, 1, 1, 2).
row_run(9, 2, 3, 8).
row_run(9, 3, 1, 2).

% Row 10: [(1,2), (3,8), (1,2)]
row_run(10, 1, 1, 2).
row_run(10, 2, 3, 8).
row_run(10, 3, 1, 2).

% Row 11: [(1,2), (2,6), (3,8), (2,6), (1,2)]
row_run(11, 1, 1, 2).
row_run(11, 2, 2, 6).
row_run(11, 3, 3, 8).
row_run(11, 4, 2, 6).
row_run(11, 5, 1, 2).

% Row 12: [(1,2), (2,6), (3,8), (2,6), (1,2)]
row_run(12, 1, 1, 2).
row_run(12, 2, 2, 6).
row_run(12, 3, 3, 8).
row_run(12, 4, 2, 6).
row_run(12, 5, 1, 2).

% Row 13: [(1,2), (2,6), (3,8), (2,6), (1,2)]
row_run(13, 1, 1, 2).
row_run(13, 2, 2, 6).
row_run(13, 3, 3, 8).
row_run(13, 4, 2, 6).
row_run(13, 5, 1, 2).

% Row 14: [(1,2), (2,6), (3,8), (2,6), (1,2)]
row_run(14, 1, 1, 2).
row_run(14, 2, 2, 6).
row_run(14, 3, 3, 8).
row_run(14, 4, 2, 6).
row_run(14, 5, 1, 2).

% Row 15: [(1,2), (3,8), (1,2)]
row_run(15, 1, 1, 2).
row_run(15, 2, 3, 8).
row_run(15, 3, 1, 2).

% Row 16: [(1,2), (3,8), (1,2)]
row_run(16, 1, 1, 2).
row_run(16, 2, 3, 8).
row_run(16, 3, 1, 2).

% Row 17: [(1,2), (2,4), (1,2)]
row_run(17, 1, 1, 2).
row_run(17, 2, 2, 4).
row_run(17, 3, 1, 2).

% Row 18: [(1,2), (2,4), (1,2)]
row_run(18, 1, 1, 2).
row_run(18, 2, 2, 4).
row_run(18, 3, 1, 2).

% Row 19: [(1,2), (2,4), (1,2)]
row_run(19, 1, 1, 2).
row_run(19, 2, 2, 4).
row_run(19, 3, 1, 2).

% Row 20: [(1,2), (2,4), (1,2)]
row_run(20, 1, 1, 2).
row_run(20, 2, 2, 4).
row_run(20, 3, 1, 2).

% Row 21: [(1,2), (2,4), (1,2)]
row_run(21, 1, 1, 2).
row_run(21, 2, 2, 4).
row_run(21, 3, 1, 2).

% Row 22: [(1,2), (2,4), (1,2)]
row_run(22, 1, 1, 2).
row_run(22, 2, 2, 4).
row_run(22, 3, 1, 2).

% Row 23: [(1,10), (2,4), (1,10)]
row_run(23, 1, 1, 10).
row_run(23, 2, 2, 4).
row_run(23, 3, 1, 10).

% Row 24: [(1,10), (2,4), (1,10)]
row_run(24, 1, 1, 10).
row_run(24, 2, 2, 4).
row_run(24, 3, 1, 10).

% Column run clues (column, run_index, color, length)
% Column 1: [(1,24)]
col_run(1, 1, 1, 24).

% Column 2: [(1,24)]
col_run(2, 1, 1, 24).

% Column 3: [(1,2), (2,4), (1,2)]
col_run(3, 1, 1, 2).
col_run(3, 2, 2, 4).
col_run(3, 3, 1, 2).

% Column 4: [(1,2), (2,4), (1,2)]
col_run(4, 1, 1, 2).
col_run(4, 2, 2, 4).
col_run(4, 3, 1, 2).

% Column 5: [(1,2), (2,4), (1,2)]
col_run(5, 1, 1, 2).
col_run(5, 2, 2, 4).
col_run(5, 3, 1, 2).

% Column 6: [(1,2), (2,4), (1,2)]
col_run(6, 1, 1, 2).
col_run(6, 2, 2, 4).
col_run(6, 3, 1, 2).

% Column 7: [(1,2), (2,4), (1,2)]
col_run(7, 1, 1, 2).
col_run(7, 2, 2, 4).
col_run(7, 3, 1, 2).

% Column 8: [(1,2), (2,4), (1,2)]
col_run(8, 1, 1, 2).
col_run(8, 2, 2, 4).
col_run(8, 3, 1, 2).

% Column 9: [(1,2), (3,8), (1,2)]
col_run(9, 1, 1, 2).
col_run(9, 2, 3, 8).
col_run(9, 3, 1, 2).

% Column 10: [(1,2), (3,8), (1,2)]
col_run(10, 1, 1, 2).
col_run(10, 2, 3, 8).
col_run(10, 3, 1, 2).

% Column 11: [(2,8), (3,8), (2,8)]
col_run(11, 1, 2, 8).
col_run(11, 2, 3, 8).
col_run(11, 3, 2, 8).

% Column 12: [(2,8), (3,8), (2,8)]
col_run(12, 1, 2, 8).
col_run(12, 2, 3, 8).
col_run(12, 3, 2, 8).

% Column 13: [(2,8), (3,8), (2,8)]
col_run(13, 1, 2, 8).
col_run(13, 2, 3, 8).
col_run(13, 3, 2, 8).

% Column 14: [(2,8), (3,8), (2,8)]
col_run(14, 1, 2, 8).
col_run(14, 2, 3, 8).
col_run(14, 3, 2, 8).

% Column 15: [(1,2), (3,8), (1,2)]
col_run(15, 1, 1, 2).
col_run(15, 2, 3, 8).
col_run(15, 3, 1, 2).

% Column 16: [(1,2), (3,8), (1,2)]
col_run(16, 1, 1, 2).
col_run(16, 2, 3, 8).
col_run(16, 3, 1, 2).

% Column 17: [(1,2), (2,4), (1,2)]
col_run(17, 1, 1, 2).
col_run(17, 2, 2, 4).
col_run(17, 3, 1, 2).

% Column 18: [(1,2), (2,4), (1,2)]
col_run(18, 1, 1, 2).
col_run(18, 2, 2, 4).
col_run(18, 3, 1, 2).

% Column 19: [(1,2), (2,4), (1,2)]
col_run(19, 1, 1, 2).
col_run(19, 2, 2, 4).
col_run(19, 3, 1, 2).

% Column 20: [(1,2), (2,4), (1,2)]
col_run(20, 1, 1, 2).
col_run(20, 2, 2, 4).
col_run(20, 3, 1, 2).

% Column 21: [(1,2), (2,4), (1,2)]
col_run(21, 1, 1, 2).
col_run(21, 2, 2, 4).
col_run(21, 3, 1, 2).

% Column 22: [(1,2), (2,4), (1,2)]
col_run(22, 1, 1, 2).
col_run(22, 2, 2, 4).
col_run(22, 3, 1, 2).

% Column 23: [(1,24)]
col_run(23, 1, 1, 24).

% Column 24: [(1,24)]
col_run(24, 1, 1, 24).

% Main diagonal sequence (position 0..23)
main_diag(0, 1).
main_diag(1, 1).
main_diag(2, 0).
main_diag(3, 0).
main_diag(4, 0).
main_diag(5, 0).
main_diag(6, 0).
main_diag(7, 0).
main_diag(8, 3).
main_diag(9, 3).
main_diag(10, 3).
main_diag(11, 3).
main_diag(12, 3).
main_diag(13, 3).
main_diag(14, 3).
main_diag(15, 3).
main_diag(16, 0).
main_diag(17, 0).
main_diag(18, 0).
main_diag(19, 0).
main_diag(20, 0).
main_diag(21, 0).
main_diag(22, 1).
main_diag(23, 1).

% Anti-diagonal sequence (position 0..23)
anti_diag(0, 1).
anti_diag(1, 1).
anti_diag(2, 0).
anti_diag(3, 0).
anti_diag(4, 0).
anti_diag(5, 0).
anti_diag(6, 0).
anti_diag(7, 0).
anti_diag(8, 3).
anti_diag(9, 3).
anti_diag(10, 3).
anti_diag(11, 3).
anti_diag(12, 3).
anti_diag(13, 3).
anti_diag(14, 3).
anti_diag(15, 3).
anti_diag(16, 0).
anti_diag(17, 0).
anti_diag(18, 0).
anti_diag(19, 0).
anti_diag(20, 0).
anti_diag(21, 0).
anti_diag(22, 1).
anti_diag(23, 1).

% Main diagonal constraint: color(X,X,C) must match main_diag(X,C)
:- size(N), X = 0..N-1, color(X, X, C), main_diag(X, C1), C != C1.

% Anti-diagonal constraint: color(X,N-1-X,C) must match anti_diag(X,C)
:- size(N), X = 0..N-1, color(X, N-1-X, C), anti_diag(X, C1), C != C1.

% Helper: run_start(R, RunIdx, StartPos) means run starts at position StartPos in row R
run_start(R, RunIdx, StartPos) :-
    size(N),
    row_run(R, RunIdx, Color, Length),
    StartPos >= 0,
    StartPos + Length - 1 < N,
    color(R, StartPos, Color),
    color(R, StartPos+Length-1, Color),
    #count{ P : P = StartPos..StartPos+Length-1, color(R, P, Color) } = Length.

% Each run must have exactly one start position
:- row_run(R, RunIdx, Color, Length), size(N), #count{ S : run_start(R, RunIdx, S) } != 1.

% Runs in a row must not overlap and must be in order
:- row_run(R, RunIdx1, C1, L1), row_run(R, RunIdx2, C2, L2), RunIdx1 < RunIdx2,
   run_start(R, RunIdx1, S1), run_start(R, RunIdx2, S2), S1 + L1 > S2.

% Cells not in any run must be white (0)
in_any_row_run(R, C) :-
    size(N),
    row_run(R, RunIdx, Color, Length),
    run_start(R, RunIdx, StartPos),
    C >= StartPos, C < StartPos + Length,
    color(R, C, Color).

:- size(N), R = 1..N, C = 1..N,
   not in_any_row_run(R, C),
   color(R, C, Col), Col != 0.

% Helper: run_start_col(C, RunIdx, StartPos) means run starts at position StartPos in column C
run_start_col(C, RunIdx, StartPos) :-
    size(N),
    col_run(C, RunIdx, Color, Length),
    StartPos >= 0,
    StartPos + Length - 1 < N,
    color(StartPos, C, Color),
    color(StartPos+Length-1, C, Color),
    #count{ P : P = StartPos..StartPos+Length-1, color(P, C, Color) } = Length.

% Each run must have exactly one start position
:- col_run(C, RunIdx, Color, Length), size(N), #count{ S : run_start_col(C, RunIdx, S) } != 1.

% Runs in a column must not overlap and must be in order
:- col_run(C, RunIdx1, C1, L1), col_run(C, RunIdx2, C2, L2), RunIdx1 < RunIdx2,
   run_start_col(C, RunIdx1, S1), run_start_col(C, RunIdx2, S2), S1 + L1 > S2.

% Cells not in any column run must be white (0)
in_any_col_run(R, C) :-
    size(N),
    col_run(C, RunIdx, Color, Length),
    run_start_col(C, RunIdx, StartPos),
    R >= StartPos, R < StartPos + Length,
    color(R, C, Color).

:- size(N), R = 1..N, C = 1..N,
   not in_any_col_run(R, C),
   color(R, C, Col), Col != 0.

% Ensure runs are separated by at least one different color (or white)
% For rows: between runs, there must be at least one cell that is not the run color
:- row_run(R, RunIdx1, Color, L1), row_run(R, RunIdx2, Color, L2),
   RunIdx1 < RunIdx2,
   run_start(R, RunIdx1, S1), run_start(R, RunIdx2, S2),
   S1 + L1 >= S2.

% For columns: between runs, there must be at least one cell that is not the run color
:- col_run(C, RunIdx1, Color, L1), col_run(C, RunIdx2, Color, L2),
   RunIdx1 < RunIdx2,
   run_start_col(C, RunIdx1, S1), run_start_col(C, RunIdx2, S2),
   S1 + L1 >= S2.

% Show the grid coloring
#show color/3.