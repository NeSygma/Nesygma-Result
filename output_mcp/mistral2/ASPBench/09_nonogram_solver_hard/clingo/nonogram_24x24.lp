%% Grid size and palette
size(24).
color(0..3).  % 0=white, 1=red, 2=green, 3=blue

%% Declare all cells
cell(X,Y) :- row(X), col(Y).
row(R) :- R = 0..23.
col(C) :- C = 0..23.

%% Main diagonal: grid[i][i] = seq[i]
main_diagonal_seq(0,1). main_diagonal_seq(1,1).
main_diagonal_seq(2,0). main_diagonal_seq(3,0).
main_diagonal_seq(4,0). main_diagonal_seq(5,0).
main_diagonal_seq(6,0). main_diagonal_seq(7,0).
main_diagonal_seq(8,3). main_diagonal_seq(9,3).
main_diagonal_seq(10,3). main_diagonal_seq(11,3).
main_diagonal_seq(12,3). main_diagonal_seq(13,3).
main_diagonal_seq(14,3). main_diagonal_seq(15,3).
main_diagonal_seq(16,0). main_diagonal_seq(17,0).
main_diagonal_seq(18,0). main_diagonal_seq(19,0).
main_diagonal_seq(20,0). main_diagonal_seq(21,0).
main_diagonal_seq(22,1). main_diagonal_seq(23,1).

%% Anti-diagonal: grid[i][23-i] = seq[i]
anti_diagonal_seq(0,1). anti_diagonal_seq(1,1).
anti_diagonal_seq(2,0). anti_diagonal_seq(3,0).
anti_diagonal_seq(4,0). anti_diagonal_seq(5,0).
anti_diagonal_seq(6,0). anti_diagonal_seq(7,0).
anti_diagonal_seq(8,3). anti_diagonal_seq(9,3).
anti_diagonal_seq(10,3). anti_diagonal_seq(11,3).
anti_diagonal_seq(12,3). anti_diagonal_seq(13,3).
anti_diagonal_seq(14,3). anti_diagonal_seq(15,3).
anti_diagonal_seq(16,0). anti_diagonal_seq(17,0).
anti_diagonal_seq(18,0). anti_diagonal_seq(19,0).
anti_diagonal_seq(20,0). anti_diagonal_seq(21,0).
anti_diagonal_seq(22,1). anti_diagonal_seq(23,1).

%% Main diagonal constraint
:- cell(I,I), color_at(I,I,C), not main_diagonal_seq(I,C).
:- main_diagonal_seq(I,C), not color_at(I,I,C).

%% Anti-diagonal constraint
:- cell(I,J), J = 23 - I, color_at(I,J,C), not anti_diagonal_seq(I,C).
:- anti_diagonal_seq(I,C), not color_at(I,23-I,C).

%% Each cell has exactly one color
1 { color_at(X,Y,C) : color(C) } 1 :- cell(X,Y).

%% Row run clues (color, length)
%% Format: run_in_row(Row, Color, Length)

%% Row 0: [(1,10), (2,4), (1,10)]
run_in_row(0,1,10). run_in_row(0,2,4). run_in_row(0,1,10).
%% Row 1: [(1,10), (2,4), (1,10)]
run_in_row(1,1,10). run_in_row(1,2,4). run_in_row(1,1,10).
%% Row 2: [(1,2), (2,4), (1,2)]
run_in_row(2,1,2). run_in_row(2,2,4). run_in_row(2,1,2).
%% Row 3: [(1,2), (2,4), (1,2)]
run_in_row(3,1,2). run_in_row(3,2,4). run_in_row(3,1,2).
%% Row 4: [(1,2), (2,4), (1,2)]
run_in_row(4,1,2). run_in_row(4,2,4). run_in_row(4,1,2).
%% Row 5: [(1,2), (2,4), (1,2)]
run_in_row(5,1,2). run_in_row(5,2,4). run_in_row(5,1,2).
%% Row 6: [(1,2), (2,4), (1,2)]
run_in_row(6,1,2). run_in_row(6,2,4). run_in_row(6,1,2).
%% Row 7: [(1,2), (2,4), (1,2)]
run_in_row(7,1,2). run_in_row(7,2,4). run_in_row(7,1,2).
%% Row 8: [(1,2), (3,8), (1,2)]
run_in_row(8,1,2). run_in_row(8,3,8). run_in_row(8,1,2).
%% Row 9: [(1,2), (3,8), (1,2)]
run_in_row(9,1,2). run_in_row(9,3,8). run_in_row(9,1,2).
%% Row 10: [(1,2), (2,6), (3,8), (2,6), (1,2)]
run_in_row(10,1,2). run_in_row(10,2,6). run_in_row(10,3,8). run_in_row(10,2,6). run_in_run(10,1,2).
%% Row 11: [(1,2), (2,6), (3,8), (2,6), (1,2)]
run_in_row(11,1,2). run_in_row(11,2,6). run_in_row(11,3,8). run_in_row(11,2,6). run_in_row(11,1,2).
%% Row 12: [(1,2), (2,6), (3,8), (2,6), (1,2)]
run_in_row(12,1,2). run_in_row(12,2,6). run_in_row(12,3,8). run_in_row(12,2,6). run_in_row(12,1,2).
%% Row 13: [(1,2), (2,6), (3,8), (2,6), (1,2)]
run_in_row(13,1,2). run_in_row(13,2,6). run_in_row(13,3,8). run_in_row(13,2,6). run_in_row(13,1,2).
%% Row 14: [(1,2), (3,8), (1,2)]
run_in_row(14,1,2). run_in_row(14,3,8). run_in_row(14,1,2).
%% Row 15: [(1,2), (3,8), (1,2)]
run_in_row(15,1,2). run_in_row(15,3,8). run_in_row(15,1,2).
%% Row 16: [(1,2), (2,4), (1,2)]
run_in_row(16,1,2). run_in_row(16,2,4). run_in_row(16,1,2).
%% Row 17: [(1,2), (2,4), (1,2)]
run_in_row(17,1,2). run_in_row(17,2,4). run_in_row(17,1,2).
%% Row 18: [(1,2), (2,4), (1,2)]
run_in_row(18,1,2). run_in_row(18,2,4). run_in_row(18,1,2).
%% Row 19: [(1,2), (2,4), (1,2)]
run_in_row(19,1,2). run_in_row(19,2,4). run_in_row(19,1,2).
%% Row 20: [(1,2), (2,4), (1,2)]
run_in_row(20,1,2). run_in_row(20,2,4). run_in_row(20,1,2).
%% Row 21: [(1,2), (2,4), (1,2)]
run_in_row(21,1,2). run_in_row(21,2,4). run_in_row(21,1,2).
%% Row 22: [(1,10), (2,4), (1,10)]
run_in_row(22,1,10). run_in_row(22,2,4). run_in_row(22,1,10).
%% Row 23: [(1,10), (2,4), (1,10)]
run_in_row(23,1,10). run_in_row(23,2,4). run_in_row(23,1,10).

%% Column run clues (color, length)
%% Format: run_in_col(Col, Color, Length)

%% Col 0: [(1,24)]
run_in_col(0,1,24).
%% Col 1: [(1,24)]
run_in_col(1,1,24).
%% Col 2: [(1,2), (2,4), (1,2)]
run_in_col(2,1,2). run_in_col(2,2,4). run_in_col(2,1,2).
%% Col 3: [(1,2), (2,4), (1,2)]
run_in_col(3,1,2). run_in_col(3,2,4). run_in_col(3,1,2).
%% Col 4: [(1,2), (2,4), (1,2)]
run_in_col(4,1,2). run_in_col(4,2,4). run_in_col(4,1,2).
%% Col 5: [(1,2), (2,4), (1,2)]
run_in_col(5,1,2). run_in_col(5,2,4). run_in_col(5,1,2).
%% Col 6: [(1,2), (2,4), (1,2)]
run_in_col(6,1,2). run_in_col(6,2,4). run_in_col(6,1,2).
%% Col 7: [(1,2), (2,4), (1,2)]
run_in_col(7,1,2). run_in_col(7,2,4). run_in_col(7,1,2).
%% Col 8: [(1,2), (3,8), (1,2)]
run_in_col(8,1,2). run_in_col(8,3,8). run_in_col(8,1,2).
%% Col 9: [(1,2), (3,8), (1,2)]
run_in_col(9,1,2). run_in_col(9,3,8). run_in_col(9,1,2).
%% Col 10: [(2,8), (3,8), (2,8)]
run_in_col(10,2,8). run_in_col(10,3,8). run_in_col(10,2,8).
%% Col 11: [(2,8), (3,8), (2,8)]
run_in_col(11,2,8). run_in_col(11,3,8). run_in_col(11,2,8).
%% Col 12: [(2,8), (3,8), (2,8)]
run_in_col(12,2,8). run_in_col(12,3,8). run_in_col(12,2,8).
%% Col 13: [(2,8), (3,8), (2,8)]
run_in_col(13,2,8). run_in_col(13,3,8). run_in_col(13,2,8).
%% Col 14: [(1,2), (3,8), (1,2)]
run_in_col(14,1,2). run_in_col(14,3,8). run_in_col(14,1,2).
%% Col 15: [(1,2), (3,8), (1,2)]
run_in_col(15,1,2). run_in_col(15,3,8). run_in_col(15,1,2).
%% Col 16: [(1,2), (2,4), (1,2)]
run_in_col(16,1,2). run_in_col(16,2,4). run_in_col(16,1,2).
%% Col 17: [(1,2), (2,4), (1,2)]
run_in_col(17,1,2). run_in_col(17,2,4). run_in_col(17,1,2).
%% Col 18: [(1,2), (2,4), (1,2)]
run_in_col(18,1,2). run_in_col(18,2,4). run_in_col(18,1,2).
%% Col 19: [(1,2), (2,4), (1,2)]
run_in_col(19,1,2). run_in_col(19,2,4). run_in_col(19,1,2).
%% Col 20: [(1,2), (2,4), (1,2)]
run_in_col(20,1,2). run_in_col(20,2,4). run_in_col(20,1,2).
%% Col 21: [(1,2), (2,4), (1,2)]
run_in_col(21,1,2). run_in_col(21,2,4). run_in_col(21,1,2).
%% Col 22: [(1,24)]
run_in_col(22,1,24).
%% Col 23: [(1,24)]
run_in_col(23,1,24).

%% Helper: position of run_in_row(R,C,L) in the sequence for row R
run_index(R,Idx,C,L) :- run_in_row(R,C,L), Idx = #count{ (C2,L2) : run_in_row(R,C2,L2), (C2,L2) < (C,L) }.

%% Helper: position of run_in_col(C,C2,L) in the sequence for column C
col_run_index(C,Idx,C2,L) :- run_in_col(C,C2,L), Idx = #count{ (C3,L2) : run_in_col(C,C3,L2), (C3,L2) < (C2,L) }.

%% For each row, enforce that runs appear in order with exact lengths
%% and all other cells are white

%% We'll use a choice rule to place runs and enforce constraints

%% For each row, define the start position of each run
max_start_row(R,L,S) :- run_in_row(R,_,L), S = 24 - L.
{ run_start(R,C,L,S) : S = 0..Smax } :- run_in_row(R,C,L), max_start_row(R,L,Smax).

%% A run must be placed exactly once
:- run_in_row(R,C,L), not run_start(R,C,L,_).

%% Runs in the same row must not overlap
:- run_start(R,C1,L1,S1), run_start(R,C2,L2,S2), C1 != C2, S1 < S2, S1+L1 > S2.
:- run_start(R,C1,L1,S1), run_start(R,C2,L2,S2), C1 != C2, S2 < S1, S2+L2 > S1.

%% Runs must appear in the correct order (by their index)
:- run_index(R,Idx1,C1,L1), run_index(R,Idx2,C2,L2), Idx1 < Idx2,
   run_start(R,C1,L1,S1), run_start(R,C2,L2,S2), S1+L1 > S2.

%% Cells in a run must have the correct color
:- run_start(R,C,L,S), X = R, Y = S..(S+L-1), not color_at(X,Y,C).

%% Cells not in any run must be white (0)
:- cell(R,Y), not in_any_row_run(R,Y), color_at(R,Y,C), C != 0.

%% Helper: a cell is in some run in its row
in_any_row_run(R,Y) :- run_start(R,_,L,S), Y >= S, Y < S+L, row(R), col(Y).

%% Similarly for columns
max_start_col(C,L,S) :- run_in_col(C,_,L), S = 24 - L.
{ col_run_start(C,C2,L,S) : S = 0..Smax } :- run_in_col(C,C2,L), max_start_col(C,L,Smax).
:- run_in_col(C,C2,L), not col_run_start(C,C2,L,_).
:- col_run_start(C1,C2,L1,S1), col_run_start(C,C2,L2,S2), C1 != C, S1 < S2, S1+L1 > S2.
:- col_run_start(C1,C2,L1,S1), col_run_start(C,C2,L2,S2), C1 != C, S2 < S1, S2+L2 > S1.
:- col_run_index(C,Idx1,C2,L1), col_run_index(C,Idx2,C3,L2), Idx1 < Idx2,
   col_run_start(C,C2,L1,S1), col_run_start(C,C3,L2,S2), S1+L1 > S2.
:- col_run_start(C,C2,L,S), X = S..(S+L-1), Y = C, not color_at(X,Y,C2).
:- cell(X,C), not in_any_col_run(X,C), color_at(X,C,C2), C2 != 0.

%% Helper: a cell is in some run in its column
in_any_col_run(X,C) :- col_run_start(_,_,L,S), X >= S, X < S+L, Y = C, col(Y), row(X).

%% Show the solution
#show color_at/3.