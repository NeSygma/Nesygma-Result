% Nonogram puzzle: 5x5 grid with row and column clues

% Grid size
row(1..5).
col(1..5).

% Row clues: row_clue(R, Length, GroupNumber)
% GroupNumber is used to order groups in a row
row_clue(1, 2, 1).
row_clue(2, 1, 1).
row_clue(3, 3, 1).
row_clue(4, 1, 1).
row_clue(4, 1, 2).
row_clue(5, 2, 1).

% Column clues: col_clue(C, Length, GroupNumber)
col_clue(1, 1, 1).
col_clue(1, 1, 2).
col_clue(2, 1, 1).
col_clue(2, 3, 2).
col_clue(3, 2, 1).
col_clue(4, 1, 1).
col_clue(5, 1, 1).

% Choice rule: assign values to cells (0 or 1)
1 { cell(R, C, 0) ; cell(R, C, 1) } 1 :- row(R), col(C).

% A cell is black if it has value 1
black(R, C) :- cell(R, C, 1).

% A cell is white if it has value 0
white(R, C) :- cell(R, C, 0).

% ========== ROW CONSTRAINTS ==========

% A group starts at C in row R if:
% - The cell is black
% - It is the first cell in the row, or the previous cell is white
group_starts_row(R, C) :-
    row(R), col(C),
    black(R, C),
    (C = 1 ; white(R, C-1)).

% A group ends at C in row R if:
% - The cell is black
% - It is the last cell in the row, or the next cell is white
group_ends_row(R, C) :-
    row(R), col(C),
    black(R, C),
    (C = 5 ; white(R, C+1)).

% Define the length of a group in a row
% A group starting at C1 and ending at C2 has length C2 - C1 + 1
group_length_row(R, C1, C2) :-
    row(R), col(C1), col(C2),
    group_starts_row(R, C1),
    group_ends_row(R, C2),
    C1 <= C2,
    #count{ C : C1 <= C, C <= C2, black(R, C) } = (C2 - C1 + 1).

% Ensure that the number of groups in a row matches the number of clues
:- row(R),
   N != #count{ L, G : row_clue(R, L, G) },
   N = #count{ C1, C2 : group_length_row(R, C1, C2) }.

% Ensure that each group in a row matches a clue
:- row(R), row_clue(R, L, G),
   not group_length_row(R, _, _; L).

% ========== COLUMN CONSTRAINTS ==========

% A group starts at R in column C if:
% - The cell is black
% - It is the first cell in the column, or the previous cell is white
group_starts_col(C, R) :-
    col(C), row(R),
    black(R, C),
    (R = 1 ; white(R-1, C)).

% A group ends at R in column C if:
% - The cell is black
% - It is the last cell in the column, or the next cell is white
group_ends_col(C, R) :-
    col(C), row(R),
    black(R, C),
    (R = 5 ; white(R+1, C)).

% Define the length of a group in a column
group_length_col(C, R1, R2) :-
    col(C), row(R1), row(R2),
    group_starts_col(C, R1),
    group_ends_col(C, R2),
    R1 <= R2,
    #count{ R : R1 <= R, R <= R2, black(R, C) } = (R2 - R1 + 1).

% Ensure that the number of groups in a column matches the number of clues
:- col(C),
   N != #count{ L, G : col_clue(C, L, G) },
   N = #count{ R1, R2 : group_length_col(C, R1, R2) }.

% Ensure that each group in a column matches a clue
:- col(C), col_clue(C, L, G),
   not group_length_col(C, _, _; L).

% ========== GROUP SEPARATION ==========

% Ensure that groups in the same row are separated by at least one white cell
:- row(R),
   group_starts_row(R, C1),
   group_starts_row(R, C2),
   C1 < C2,
   not white(R, C) : C1 < C, C < C2.

% Ensure that groups in the same column are separated by at least one white cell
:- col(C),
   group_starts_col(C, R1),
   group_starts_col(C, R2),
   R1 < R2,
   not white(R, C) : R1 < R, R < R2.

% ========== CONSECUTIVE GROUPS ==========

% Ensure that black cells form valid groups (consecutive)
:- row(R),
   black(R, C),
   black(R, C+2),
   not black(R, C+1),
   C+2 <= 5.

:- col(C),
   black(R, C),
   black(R+2, C),
   not black(R+1, C),
   R+2 <= 5.

% ========== SHOW THE GRID ==========
#show cell/3.