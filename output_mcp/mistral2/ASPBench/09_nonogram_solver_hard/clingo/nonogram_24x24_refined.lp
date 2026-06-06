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

%% Row run clues (color, length, index)
run_in_row(0,1,10,0). run_in_row(0,2,4,1). run_in_row(0,1,10,2).
run_in_row(1,1,10,0). run_in_row(1,2,4,1). run_in_row(1,1,10,2).
run_in_row(2,1,2,0). run_in_row(2,2,4,1). run_in_row(2,1,2,2).
run_in_row(3,1,2,0). run_in_row(3,2,4,1). run_in_row(3,1,2,2).
run_in_row(4,1,2,0). run_in_row(4,2,4,1). run_in_row(4,1,2,2).
run_in_row(5,1,2,0). run_in_row(5,2,4,1). run_in_row(5,1,2,2).
run_in_row(6,1,2,0). run_in_row(6,2,4,1). run_in_row(6,1,2,2).
run_in_row(7,1,2,0). run_in_row(7,2,4,1). run_in_row(7,1,2,2).
run_in_row(8,1,2,0). run_in_row(8,3,8,1). run_in_row(8,1,2,2).
run_in_row(9,1,2,0). run_in_row(9,3,8,1). run_in_row(9,1,2,2).
run_in_row(10,1,2,0). run_in_row(10,2,6,1). run_in_row(10,3,8,2). run_in_row(10,2,6,3). run_in_row(10,1,2,4).
run_in_row(11,1,2,0). run_in_row(11,2,6,1). run_in_row(11,3,8,2). run_in_row(11,2,6,3). run_in_row(11,1,2,4).
run_in_row(12,1,2,0). run_in_row(12,2,6,1). run_in_row(12,3,8,2). run_in_row(12,2,6,3). run_in_row(12,1,2,4).
run_in_row(13,1,2,0). run_in_row(13,2,6,1). run_in_row(13,3,8,2). run_in_row(13,2,6,3). run_in_row(13,1,2,4).
run_in_row(14,1,2,0). run_in_row(14,3,8,1). run_in_row(14,1,2,2).
run_in_row(15,1,2,0). run_in_row(15,3,8,1). run_in_row(15,1,2,2).
run_in_row(16,1,2,0). run_in_row(16,2,4,1). run_in_row(16,1,2,2).
run_in_row(17,1,2,0). run_in_row(17,2,4,1). run_in_row(17,1,2,2).
run_in_row(18,1,2,0). run_in_row(18,2,4,1). run_in_row(18,1,2,2).
run_in_row(19,1,2,0). run_in_row(19,2,4,1). run_in_row(19,1,2,2).
run_in_row(20,1,2,0). run_in_row(20,2,4,1). run_in_row(20,1,2,2).
run_in_row(21,1,2,0). run_in_row(21,2,4,1). run_in_row(21,1,2,2).
run_in_row(22,1,10,0). run_in_row(22,2,4,1). run_in_row(22,1,10,2).
run_in_row(23,1,10,0). run_in_row(23,2,4,1). run_in_row(23,1,10,2).

%% Column run clues (color, length, index)
run_in_col(0,1,24,0).
run_in_col(1,1,24,0).
run_in_col(2,1,2,0). run_in_col(2,2,4,1). run_in_col(2,1,2,2).
run_in_col(3,1,2,0). run_in_col(3,2,4,1). run_in_col(3,1,2,2).
run_in_col(4,1,2,0). run_in_col(4,2,4,1). run_in_col(4,1,2,2).
run_in_col(5,1,2,0). run_in_col(5,2,4,1). run_in_col(5,1,2,2).
run_in_col(6,1,2,0). run_in_col(6,2,4,1). run_in_col(6,1,2,2).
run_in_col(7,1,2,0). run_in_col(7,2,4,1). run_in_col(7,1,2,2).
run_in_col(8,1,2,0). run_in_col(8,3,8,1). run_in_col(8,1,2,2).
run_in_col(9,1,2,0). run_in_col(9,3,8,1). run_in_col(9,1,2,2).
run_in_col(10,2,8,0). run_in_col(10,3,8,1). run_in_col(10,2,8,2).
run_in_col(11,2,8,0). run_in_col(11,3,8,1). run_in_col(11,2,8,2).
run_in_col(12,2,8,0). run_in_col(12,3,8,1). run_in_col(12,2,8,2).
run_in_col(13,2,8,0). run_in_col(13,3,8,1). run_in_col(13,2,8,2).
run_in_col(14,1,2,0). run_in_col(14,3,8,1). run_in_col(14,1,2,2).
run_in_col(15,1,2,0). run_in_col(15,3,8,1). run_in_col(15,1,2,2).
run_in_col(16,1,2,0). run_in_col(16,2,4,1). run_in_col(16,1,2,2).
run_in_col(17,1,2,0). run_in_col(17,2,4,1). run_in_col(17,1,2,2).
run_in_col(18,1,2,0). run_in_col(18,2,4,1). run_in_col(18,1,2,2).
run_in_col(19,1,2,0). run_in_col(19,2,4,1). run_in_col(19,1,2,2).
run_in_col(20,1,2,0). run_in_col(20,2,4,1). run_in_col(20,1,2,2).
run_in_col(21,1,2,0). run_in_col(21,2,4,1). run_in_col(21,1,2,2).
run_in_col(22,1,24,0).
run_in_col(23,1,24,0).

%% Enforce that runs are placed correctly in rows
:- run_in_row(R,C,L,I), not run_placed_in_row(R,C,L,I).
run_placed_in_row(R,C,L,I) :- run_in_row(R,C,L,I), Y = 0..23, Y >= I, Y < I+L, color_at(R,Y,C).

%% Enforce that runs are placed correctly in columns
:- run_in_col(C,C2,L,I), not run_placed_in_col(C,C2,L,I).
run_placed_in_col(C,C2,L,I) :- run_in_col(C,C2,L,I), X = 0..23, X >= I, X < I+L, color_at(X,C,C2).

%% Ensure runs do not overlap in rows
:- run_in_row(R,C1,L1,I1), run_in_row(R,C2,L2,I2), I1 < I2, I1+L1 > I2.

%% Ensure runs do not overlap in columns
:- run_in_col(C1,C2,L1,I1), run_in_col(C2,C3,L2,I2), I1 < I2, I1+L1 > I2.

%% Cells not in any run must be white (0)
:- cell(R,Y), not in_any_row_run(R,Y), color_at(R,Y,C), C != 0.
in_any_row_run(R,Y) :- run_in_row(R,_,L,I), Y >= I, Y < I+L.

:- cell(X,C), not in_any_col_run(X,C), color_at(X,C,C2), C2 != 0.
in_any_col_run(X,C) :- run_in_col(C,_,L,I), X >= I, X < I+L.

%% Show the solution
#show color_at/3.