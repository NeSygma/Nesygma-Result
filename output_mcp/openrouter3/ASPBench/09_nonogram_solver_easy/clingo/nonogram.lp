% Nonogram 5x5 Puzzle Solver

% Domain definitions
row(1..5).
col(1..5).
cell(0). cell(1). % 0=white, 1=black

% Grid variables: grid(Row, Col) = 0 or 1
{grid(R, C) : cell(1)} :- row(R), col(C).

% Helper: check if a cell is black
is_black(R, C) :- grid(R, C) = 1.
is_white(R, C) :- grid(R, C) = 0.

% Row constraints
% Row 1: [2] - one group of 2 consecutive black cells
% Row 2: [1] - one group of 1 black cell
% Row 3: [3] - one group of 3 consecutive black cells
% Row 4: [1,1] - two groups of 1 black cell each (separated by at least one white)
% Row 5: [2] - one group of 2 consecutive black cells

% Helper: count consecutive black cells starting at position C in row R
% A group of length L starting at C means:
% - Cells C, C+1, ..., C+L-1 are black
% - Cell C-1 (if exists) is white
% - Cell C+L (if exists) is white
group_start_row(R, C, L) :-
    row(R), col(C), L >= 1,
    % All cells from C to C+L-1 are black
    is_black(R, C+I) : 0 <= I < L,
    % Cell before (if exists) is white
    (C > 1, is_white(R, C-1); C = 1),
    % Cell after (if exists) is white
    (C+L <= 5, is_white(R, C+L); C+L > 5).

% Row 1: exactly one group of length 2
:- row(1),
   #count{C : group_start_row(1, C, 2)} != 1.

% Row 2: exactly one group of length 1
:- row(2),
   #count{C : group_start_row(2, C, 1)} != 1.

% Row 3: exactly one group of length 3
:- row(3),
   #count{C : group_start_row(3, C, 3)} != 1.

% Row 4: exactly two groups of length 1, separated by at least one white
:- row(4),
   #count{C : group_start_row(4, C, 1)} != 2.

% Row 5: exactly one group of length 2
:- row(5),
   #count{C : group_start_row(5, C, 2)} != 1.

% Column constraints
% Column 1: [1,1] - two groups of 1 black cell each (separated)
% Column 2: [1,3] - first one group of 1, then one group of 3 (separated)
% Column 3: [2] - one group of 2 consecutive black cells
% Column 4: [1] - one group of 1 black cell
% Column 5: [1] - one group of 1 black cell

% Helper: count consecutive black cells starting at position R in column C
group_start_col(C, R, L) :-
    col(C), row(R), L >= 1,
    % All cells from R to R+L-1 are black
    is_black(R+I, C) : 0 <= I < L,
    % Cell before (if exists) is white
    (R > 1, is_white(R-1, C); R = 1),
    % Cell after (if exists) is white
    (R+L <= 5, is_white(R+L, C); R+L > 5).

% Column 1: exactly two groups of length 1
:- col(1),
   #count{R : group_start_col(1, R, 1)} != 2.

% Column 2: exactly one group of length 1 and one group of length 3
:- col(2),
   #count{R : group_start_col(2, R, 1)} != 1;
   #count{R : group_start_col(2, R, 3)} != 1.

% Column 3: exactly one group of length 2
:- col(3),
   #count{R : group_start_col(3, R, 2)} != 1.

% Column 4: exactly one group of length 1
:- col(4),
   #count{R : group_start_col(4, R, 1)} != 1.

% Column 5: exactly one group of length 1
:- col(5),
   #count{R : group_start_col(5, R, 1)} != 1.

% Show the grid
#show grid/2.