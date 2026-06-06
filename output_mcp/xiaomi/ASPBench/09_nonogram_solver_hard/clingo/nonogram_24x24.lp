% Grid size and domains
n(24).
row(1..24).
col(1..24).
color(0). color(1). color(2). color(3).

% ===== ROW CLUES =====
% Row 1: [(1,10), (2,4), (1,10)]
row_run(1,1,1,10). row_run(1,2,2,4). row_run(1,3,1,10).
% Row 2: [(1,10), (2,4), (1,10)]
row_run(2,1,1,10). row_run(2,2,2,4). row_run(2,3,1,10).
% Row 3: [(1,2), (2,4), (1,2)]
row_run(3,1,1,2). row_run(3,2,2,4). row_run(3,3,1,2).
% Row 4: [(1,2), (2,4), (1,2)]
row_run(4,1,1,2). row_run(4,2,2,4). row_run(4,3,1,2).
% Row 5: [(1,2), (2,4), (1,2)]
row_run(5,1,1,2). row_run(5,2,2,4). row_run(5,3,1,2).
% Row 6: [(1,2), (2,4), (1,2)]
row_run(6,1,1,2). row_run(6,2,2,4). row_run(6,3,1,2).
% Row 7: [(1,2), (2,4), (1,2)]
row_run(7,1,1,2). row_run(7,2,2,4). row_run(7,3,1,2).
% Row 8: [(1,2), (2,4), (1,2)]
row_run(8,1,1,2). row_run(8,2,2,4). row_run(8,3,1,2).
% Row 9: [(1,2), (3,8), (1,2)]
row_run(9,1,1,2). row_run(9,2,3,8). row_run(9,3,1,2).
% Row 10: [(1,2), (3,8), (1,2)]
row_run(10,1,1,2). row_run(10,2,3,8). row_run(10,3,1,2).
% Row 11: [(1,2), (2,6), (3,8), (2,6), (1,2)]
row_run(11,1,1,2). row_run(11,2,2,6). row_run(11,3,3,8). row_run(11,4,2,6). row_run(11,5,1,2).
% Row 12: [(1,2), (2,6), (3,8), (2,6), (1,2)]
row_run(12,1,1,2). row_run(12,2,2,6). row_run(12,3,3,8). row_run(12,4,2,6). row_run(12,5,1,2).
% Row 13: [(1,2), (2,6), (3,8), (2,6), (1,2)]
row_run(13,1,1,2). row_run(13,2,2,6). row_run(13,3,3,8). row_run(13,4,2,6). row_run(13,5,1,2).
% Row 14: [(1,2), (2,6), (3,8), (2,6), (1,2)]
row_run(14,1,1,2). row_run(14,2,2,6). row_run(14,3,3,8). row_run(14,4,2,6). row_run(14,5,1,2).
% Row 15: [(1,2), (3,8), (1,2)]
row_run(15,1,1,2). row_run(15,2,3,8). row_run(15,3,1,2).
% Row 16: [(1,2), (3,8), (1,2)]
row_run(16,1,1,2). row_run(16,2,3,8). row_run(16,3,1,2).
% Row 17: [(1,2), (2,4), (1,2)]
row_run(17,1,1,2). row_run(17,2,2,4). row_run(17,3,1,2).
% Row 18: [(1,2), (2,4), (1,2)]
row_run(18,1,1,2). row_run(18,2,2,4). row_run(18,3,1,2).
% Row 19: [(1,2), (2,4), (1,2)]
row_run(19,1,1,2). row_run(19,2,2,4). row_run(19,3,1,2).
% Row 20: [(1,2), (2,4), (1,2)]
row_run(20,1,1,2). row_run(20,2,2,4). row_run(20,3,1,2).
% Row 21: [(1,2), (2,4), (1,2)]
row_run(21,1,1,2). row_run(21,2,2,4). row_run(21,3,1,2).
% Row 22: [(1,2), (2,4), (1,2)]
row_run(22,1,1,2). row_run(22,2,2,4). row_run(22,3,1,2).
% Row 23: [(1,10), (2,4), (1,10)]
row_run(23,1,1,10). row_run(23,2,2,4). row_run(23,3,1,10).
% Row 24: [(1,10), (2,4), (1,10)]
row_run(24,1,1,10). row_run(24,2,2,4). row_run(24,3,1,10).

% ===== COLUMN CLUES =====
% Column 1: [(1,24)]
col_run(1,1,1,24).
% Column 2: [(1,24)]
col_run(2,1,1,24).
% Column 3: [(1,2), (2,4), (1,2)]
col_run(3,1,1,2). col_run(3,2,2,4). col_run(3,3,1,2).
% Column 4: [(1,2), (2,4), (1,2)]
col_run(4,1,1,2). col_run(4,2,2,4). col_run(4,3,1,2).
% Column 5: [(1,2), (2,4), (1,2)]
col_run(5,1,1,2). col_run(5,2,2,4). col_run(5,3,1,2).
% Column 6: [(1,2), (2,4), (1,2)]
col_run(6,1,1,2). col_run(6,2,2,4). col_run(6,3,1,2).
% Column 7: [(1,2), (2,4), (1,2)]
col_run(7,1,1,2). col_run(7,2,2,4). col_run(7,3,1,2).
% Column 8: [(1,2), (2,4), (1,2)]
col_run(8,1,1,2). col_run(8,2,2,4). col_run(8,3,1,2).
% Column 9: [(1,2), (3,8), (1,2)]
col_run(9,1,1,2). col_run(9,2,3,8). col_run(9,3,1,2).
% Column 10: [(1,2), (3,8), (1,2)]
col_run(10,1,1,2). col_run(10,2,3,8). col_run(10,3,1,2).
% Column 11: [(2,8), (3,8), (2,8)]
col_run(11,1,2,8). col_run(11,2,3,8). col_run(11,3,2,8).
% Column 12: [(2,8), (3,8), (2,8)]
col_run(12,1,2,8). col_run(12,2,3,8). col_run(12,3,2,8).
% Column 13: [(2,8), (3,8), (2,8)]
col_run(13,1,2,8). col_run(13,2,3,8). col_run(13,3,2,8).
% Column 14: [(2,8), (3,8), (2,8)]
col_run(14,1,2,8). col_run(14,2,3,8). col_run(14,3,2,8).
% Column 15: [(1,2), (3,8), (1,2)]
col_run(15,1,1,2). col_run(15,2,3,8). col_run(15,3,1,2).
% Column 16: [(1,2), (3,8), (1,2)]
col_run(16,1,1,2). col_run(16,2,3,8). col_run(16,3,1,2).
% Column 17: [(1,2), (2,4), (1,2)]
col_run(17,1,1,2). col_run(17,2,2,4). col_run(17,3,1,2).
% Column 18: [(1,2), (2,4), (1,2)]
col_run(18,1,1,2). col_run(18,2,2,4). col_run(18,3,1,2).
% Column 19: [(1,2), (2,4), (1,2)]
col_run(19,1,1,2). col_run(19,2,2,4). col_run(19,3,1,2).
% Column 20: [(1,2), (2,4), (1,2)]
col_run(20,1,1,2). col_run(20,2,2,4). col_run(20,3,1,2).
% Column 21: [(1,2), (2,4), (1,2)]
col_run(21,1,1,2). col_run(21,2,2,4). col_run(21,3,1,2).
% Column 22: [(1,2), (2,4), (1,2)]
col_run(22,1,1,2). col_run(22,2,2,4). col_run(22,3,1,2).
% Column 23: [(1,24)]
col_run(23,1,1,24).
% Column 24: [(1,24)]
col_run(24,1,1,24).

% ===== MAIN DIAGONAL =====
main_diag(1,1). main_diag(2,1). main_diag(3,0). main_diag(4,0).
main_diag(5,0). main_diag(6,0). main_diag(7,0). main_diag(8,0).
main_diag(9,3). main_diag(10,3). main_diag(11,3). main_diag(12,3).
main_diag(13,3). main_diag(14,3). main_diag(15,3). main_diag(16,3).
main_diag(17,0). main_diag(18,0). main_diag(19,0). main_diag(20,0).
main_diag(21,0). main_diag(22,0). main_diag(23,1). main_diag(24,1).

% ===== ANTI-DIAGONAL =====
anti_diag(1,1). anti_diag(2,1). anti_diag(3,0). anti_diag(4,0).
anti_diag(5,0). anti_diag(6,0). anti_diag(7,0). anti_diag(8,0).
anti_diag(9,3). anti_diag(10,3). anti_diag(11,3). anti_diag(12,3).
anti_diag(13,3). anti_diag(14,3). anti_diag(15,3). anti_diag(16,3).
anti_diag(17,0). anti_diag(18,0). anti_diag(19,0). anti_diag(20,0).
anti_diag(21,0). anti_diag(22,0). anti_diag(23,1). anti_diag(24,1).

% ===== DERIVED DOMAINS =====
% Number of runs per row
row_num_runs(R, N) :- N = #count{I : row_run(R,I,_,_)}, row(R).
% Number of runs per column
col_num_runs(C, N) :- N = #count{I : col_run(C,I,_,_)}, col(C).

% Cumulative length of runs in a row (sum of lengths + gaps between runs)
% For row R, total colored cells = sum of lengths of all runs
row_total_len(R, TL) :- TL = #sum{L,I : row_run(R,I,_,L)}, row(R).
% For column C, total colored cells = sum of lengths of all runs
col_total_len(C, TL) :- TL = #sum{L,I : col_run(C,I,_,L)}, col(C).

% ===== CHOICE: RUN START POSITIONS =====
% For each row run, choose a starting column
% Run I in row R starts at column S
% Constraints: runs must be in order, non-overlapping, with at least 1 gap between different colors
% First run starts at some column >= 1
{ run_start_row(R, 1, S) : col(S) } 1 :- row(R).
% Subsequent runs start after previous run ends + 1 (gap)
{ run_start_row(R, I, S) : col(S) } 1 :- row(R), row_run(R,I,_,_), I > 1.

% For each column run, choose a starting row
{ run_start_col(C, 1, S) : row(S) } 1 :- col(C).
{ run_start_col(C, I, S) : row(S) } 1 :- col(C), col_run(C,I,_,_), I > 1.

% ===== CONSTRAINTS ON RUN POSITIONS =====
% Row runs must be in order: run I+1 starts after run I ends
% Run I ends at start + length - 1
row_run_end(R, I, E) :- run_start_row(R, I, S), row_run(R, I, _, L), E = S + L - 1.
% Run I+1 must start at least 1 after run I ends (gap for different color separation)
:- run_start_row(R, I, S1), row_run_end(R, I, E1), run_start_row(R, I+1, S2), S2 <= E1.
% All runs must fit within the grid
:- run_start_row(R, I, S), row_run(R, I, _, L), S + L - 1 > 24.
% First run must start at column >= 1
:- run_start_row(R, 1, S), S < 1.

% Column runs must be in order
col_run_end(C, I, E) :- run_start_col(C, I, S), col_run(C, I, _, L), E = S + L - 1.
:- run_start_col(C, I, S1), col_run_end(C, I, E1), run_start_col(C, I+1, S2), S2 <= E1.
:- run_start_col(C, I, S), col_run(C, I, _, L), S + L - 1 > 24.
:- run_start_col(C, 1, S), S < 1.

% ===== CELL ASSIGNMENT FROM ROW RUNS =====
% A cell (R,C) gets color from row run I if C is within [start, start+length-1]
cell_from_row(R, C, Clr) :- run_start_row(R, I, S), row_run(R, I, Clr, L), 
                            col(C), C >= S, C <= S + L - 1.

% ===== CELL ASSIGNMENT FROM COLUMN RUNS =====
cell_from_col(R, C, Clr) :- run_start_col(C, I, S), col_run(C, I, Clr, L),
                             row(R), R >= S, R <= S + L - 1.

% ===== FINAL CELL COLOR =====
% Cell gets color from row assignment if it's in a row run
cell(R, C, Clr) :- cell_from_row(R, C, Clr).
% Cell gets color from column assignment if it's in a column run
cell(R, C, Clr) :- cell_from_col(R, C, Clr).
% Cells not in any run are white
cell(R, C, 0) :- row(R), col(C), not cell_from_row(R, C, _), not cell_from_col(R, C, _).

% ===== CONSISTENCY CONSTRAINTS =====
% A cell cannot have two different colors
:- cell(R, C, Clr1), cell(R, C, Clr2), Clr1 != Clr2.

% ===== DIAGONAL CONSTRAINTS =====
% Main diagonal: cell(i,i) must match main_diag(i, Color)
:- main_diag(I, Clr), cell(I, I, Clr2), Clr != Clr2.

% Anti-diagonal: cell(i, 25-i) must match anti_diag(i, Color)
:- anti_diag(I, Clr), cell(I, 25-I, Clr2), Clr != Clr2.

% ===== EXHAUSTIVENESS: NO EXTRA COLORED CELLS =====
% Every colored cell must belong to some row run or column run
% This is already enforced by: cells not in any run are white

% ===== ADDITIONAL: RUNS MUST BE EXACT LENGTH =====
% Already enforced by the run_start constraints and cell assignment

% ===== SHOW =====
#show cell/3.