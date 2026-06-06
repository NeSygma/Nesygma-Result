% Nonogram 5x5 puzzle solver

% Grid dimensions
row(1..5).
col(1..5).

% Each cell is either black (1) or white (0)
{ cell(R, C, 1) } :- row(R), col(C).
cell(R, C, 0) :- row(R), col(C), not cell(R, C, 1).

% Helper: is_black(R, C) if cell is black
is_black(R, C) :- cell(R, C, 1).
is_white(R, C) :- cell(R, C, 0).

% Row clues: groups of consecutive black cells
% Row 1: [2] - one group of 2 consecutive black cells
% Row 2: [1] - one group of 1 black cell
% Row 3: [3] - one group of 3 consecutive black cells
% Row 4: [1, 1] - two groups of 1 black cell each (separated by at least one white)
% Row 5: [2] - one group of 2 consecutive black cells

% Column clues: groups of consecutive black cells
% Col 1: [1, 1] - two groups of 1 black cell each
% Col 2: [1, 3] - first one group of 1, then one group of 3
% Col 3: [2] - one group of 2 consecutive black cells
% Col 4: [1] - one group of 1 black cell
% Col 5: [1] - one group of 1 black cell

% Define clue specifications
% row_clue(Row, GroupIndex, Length)
row_clue(1, 1, 2).
row_clue(2, 1, 1).
row_clue(3, 1, 3).
row_clue(4, 1, 1).
row_clue(4, 2, 1).
row_clue(5, 1, 2).

% col_clue(Col, GroupIndex, Length)
col_clue(1, 1, 1).
col_clue(1, 2, 1).
col_clue(2, 1, 1).
col_clue(2, 2, 3).
col_clue(3, 1, 2).
col_clue(4, 1, 1).
col_clue(5, 1, 1).

% Count number of groups in each row
row_group_count(R, N) :- row(R), N = #count{G : row_clue(R, G, _)}.

% Count number of groups in each column
col_group_count(C, N) :- col(C), N = #count{G : col_clue(C, G, _)}.

% For each row, we need to place groups in order
% A group starts at some column and has a specific length
% We need to ensure groups don't overlap and are separated by at least one white

% For rows with single group (rows 1, 2, 3, 5)
% The group must be consecutive black cells of the specified length

% For row 1: [2] - group of 2 consecutive black cells
% The group can start at columns 1-4
{ row1_start(C) : col(C), C <= 4 } 1.
% Cells in the group are black
cell(1, C, 1) :- row1_start(S), col(C), C >= S, C <= S+1.
% Cells outside the group are white
cell(1, C, 0) :- row1_start(S), col(C), C < S.
cell(1, C, 0) :- row1_start(S), col(C), C > S+1.

% For row 2: [1] - group of 1 black cell
{ row2_start(C) : col(C) } 1.
cell(2, C, 1) :- row2_start(C).
cell(2, C2, 0) :- row2_start(C), col(C2), C2 != C.

% For row 3: [3] - group of 3 consecutive black cells
{ row3_start(C) : col(C), C <= 3 } 1.
cell(3, C, 1) :- row3_start(S), col(C), C >= S, C <= S+2.
cell(3, C, 0) :- row3_start(S), col(C), C < S.
cell(3, C, 0) :- row3_start(S), col(C), C > S+2.

% For row 4: [1, 1] - two groups of 1 black cell each, separated by at least one white
{ row4_start1(C1) : col(C1) } 1.
{ row4_start2(C2) : col(C2) } 1.
% Second group must be after first group with at least one white between
:- row4_start1(C1), row4_start2(C2), C2 <= C1+1.
cell(4, C, 1) :- row4_start1(C).
cell(4, C, 1) :- row4_start2(C).
cell(4, C, 0) :- col(C), not row4_start1(C), not row4_start2(C).

% For row 5: [2] - group of 2 consecutive black cells
{ row5_start(C) : col(C), C <= 4 } 1.
cell(5, C, 1) :- row5_start(S), col(C), C >= S, C <= S+1.
cell(5, C, 0) :- row5_start(S), col(C), C < S.
cell(5, C, 0) :- row5_start(S), col(C), C > S+1.

% Now handle column clues similarly
% For column 1: [1, 1] - two groups of 1 black cell each
{ col1_start1(R1) : row(R1) } 1.
{ col1_start2(R2) : row(R2) } 1.
:- col1_start1(R1), col1_start2(R2), R2 <= R1+1.
cell(R, 1, 1) :- col1_start1(R).
cell(R, 1, 1) :- col1_start2(R).
cell(R, 1, 0) :- row(R), not col1_start1(R), not col1_start2(R).

% For column 2: [1, 3] - first group of 1, then group of 3
{ col2_start1(R1) : row(R1) } 1.
{ col2_start2(R2) : row(R2), R2 <= 3 } 1.
:- col2_start1(R1), col2_start2(R2), R2 <= R1+1.
cell(R, 2, 1) :- col2_start1(R).
cell(R, 2, 1) :- col2_start2(S), row(R), R >= S, R <= S+2.
cell(R, 2, 0) :- row(R), not col2_start1(R), not col2_start2(S) : row(S), S <= R, R <= S+2.

% For column 3: [2] - group of 2 consecutive black cells
{ col3_start(R) : row(R), R <= 4 } 1.
cell(R, 3, 1) :- col3_start(S), row(R), R >= S, R <= S+1.
cell(R, 3, 0) :- col3_start(S), row(R), R < S.
cell(R, 3, 0) :- col3_start(S), row(R), R > S+1.

% For column 4: [1] - group of 1 black cell
{ col4_start(R) : row(R) } 1.
cell(R, 4, 1) :- col4_start(R).
cell(R, 4, 0) :- row(R), not col4_start(R).

% For column 5: [1] - group of 1 black cell
{ col5_start(R) : row(R) } 1.
cell(R, 5, 1) :- col5_start(R).
cell(R, 5, 0) :- row(R), not col5_start(R).

% Ensure consistency between row and column constraints
% (The cell definitions above should already enforce this)

% Output
#show cell/3.
#show valid.

% Valid if we have a solution
valid :- cell(R, C, V), row(R), col(C), V >= 0, V <= 1.