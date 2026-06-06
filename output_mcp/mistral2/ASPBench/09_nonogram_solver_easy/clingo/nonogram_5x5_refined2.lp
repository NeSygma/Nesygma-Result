% Define the grid cells (1-indexed)
cell(1..5, 1..5).

% Row clues: row_clue(R, GroupLength, GroupIndex)
% Row 1: [2] -> one group of length 2
row_clue(1, 2, 1).
% Row 2: [1] -> one group of length 1
row_clue(2, 1, 1).
% Row 3: [3] -> one group of length 3
row_clue(3, 3, 1).
% Row 4: [1, 1] -> two groups of length 1
row_clue(4, 1, 1).
row_clue(4, 1, 2).
% Row 5: [2] -> one group of length 2
row_clue(5, 2, 1).

% Column clues: col_clue(C, GroupLength, GroupIndex)
% Column 1: [1, 1] -> two groups of length 1
col_clue(1, 1, 1).
col_clue(1, 1, 2).
% Column 2: [1, 3] -> first one group of 1, then group of length 3
col_clue(2, 1, 1).
col_clue(2, 3, 2).
% Column 3: [2] -> one group of length 2
col_clue(3, 2, 1).
% Column 4: [1] -> one group of length 1
col_clue(4, 1, 1).
% Column 5: [1] -> one group of length 1
col_clue(5, 1, 1).

% Each cell is either 0 (white) or 1 (black)
1 { value(R, C, 0) ; value(R, C, 1) } 1 :- cell(R, C).

% Helper: A cell is black
black(R, C) :- value(R, C, 1).

% Helper: A cell is white
white(R, C) :- value(R, C, 0).

% Define valid row configurations

% Row 1: [2] (one group of 2)
valid_row1_1 :- black(1,1), black(1,2), white(1,3), white(1,4), white(1,5).
valid_row1_2 :- white(1,1), black(1,2), black(1,3), white(1,4), white(1,5).
valid_row1_3 :- white(1,1), white(1,2), black(1,3), black(1,4), white(1,5).
valid_row1_4 :- white(1,1), white(1,2), white(1,3), black(1,4), black(1,5).

% Row 2: [1] (one group of 1)
valid_row2_1 :- black(2,1), white(2,2), white(2,3), white(2,4), white(2,5).
valid_row2_2 :- white(2,1), black(2,2), white(2,3), white(2,4), white(2,5).
valid_row2_3 :- white(2,1), white(2,2), black(2,3), white(2,4), white(2,5).
valid_row2_4 :- white(2,1), white(2,2), white(2,3), black(2,4), white(2,5).
valid_row2_5 :- white(2,1), white(2,2), white(2,3), white(2,4), black(2,5).

% Row 3: [3] (one group of 3)
valid_row3_1 :- black(3,1), black(3,2), black(3,3), white(3,4), white(3,5).
valid_row3_2 :- white(3,1), black(3,2), black(3,3), black(3,4), white(3,5).
valid_row3_3 :- white(3,1), white(3,2), black(3,3), black(3,4), black(3,5).

% Row 4: [1, 1] (two groups of 1, separated)
valid_row4_1 :- black(4,1), white(4,2), black(4,3), white(4,4), white(4,5).
valid_row4_2 :- black(4,1), white(4,2), white(4,3), black(4,4), white(4,5).
valid_row4_3 :- black(4,1), white(4,2), white(4,3), white(4,4), black(4,5).
valid_row4_4 :- white(4,1), black(4,2), white(4,3), black(4,4), white(4,5).
valid_row4_5 :- white(4,1), black(4,2), white(4,3), white(4,4), black(4,5).
valid_row4_6 :- white(4,1), white(4,2), black(4,3), white(4,4), black(4,5).

% Row 5: [2] (one group of 2)
valid_row5_1 :- black(5,1), black(5,2), white(5,3), white(5,4), white(5,5).
valid_row5_2 :- white(5,1), black(5,2), black(5,3), white(5,4), white(5,5).
valid_row5_3 :- white(5,1), white(5,2), black(5,3), black(5,4), white(5,5).
valid_row5_4 :- white(5,1), white(5,2), white(5,3), black(5,4), black(5,5).

% Column 1: [1, 1] (two groups of 1, separated)
valid_col1_1 :- black(1,1), white(2,1), black(3,1), white(4,1), white(5,1).
valid_col1_2 :- black(1,1), white(2,1), white(3,1), black(4,1), white(5,1).
valid_col1_3 :- black(1,1), white(2,1), white(3,1), white(4,1), black(5,1).
valid_col1_4 :- white(1,1), black(2,1), white(3,1), black(4,1), white(5,1).
valid_col1_5 :- white(1,1), black(2,1), white(3,1), white(4,1), black(5,1).
valid_col1_6 :- white(1,1), white(2,1), black(3,1), white(4,1), black(5,1).

% Column 2: [1, 3] (one group of 1, then one group of 3)
valid_col2_1 :- black(1,2), white(2,2), black(3,2), black(4,2), black(5,2).
valid_col2_2 :- white(1,2), black(2,2), black(3,2), black(4,2), white(5,2).

% Column 3: [2] (one group of 2)
valid_col3_1 :- black(1,3), black(2,3), white(3,3), white(4,3), white(5,3).
valid_col3_2 :- white(1,3), black(2,3), black(3,3), white(4,3), white(5,3).
valid_col3_3 :- white(1,3), white(2,3), black(3,3), black(4,3), white(5,3).
valid_col3_4 :- white(1,3), white(2,3), white(3,3), black(4,3), black(5,3).

% Column 4: [1] (one group of 1)
valid_col4_1 :- black(1,4), white(2,4), white(3,4), white(4,4), white(5,4).
valid_col4_2 :- white(1,4), black(2,4), white(3,4), white(4,4), white(5,4).
valid_col4_3 :- white(1,4), white(2,4), black(3,4), white(4,4), white(5,4).
valid_col4_4 :- white(1,4), white(2,4), white(3,4), black(4,4), white(5,4).
valid_col4_5 :- white(1,4), white(2,4), white(3,4), white(4,4), black(5,4).

% Column 5: [1] (one group of 1)
valid_col5_1 :- black(1,5), white(2,5), white(3,5), white(4,5), white(5,5).
valid_col5_2 :- white(1,5), black(2,5), white(3,5), white(4,5), white(5,5).
valid_col5_3 :- white(1,5), white(2,5), black(3,5), white(4,5), white(5,5).
valid_col5_4 :- white(1,5), white(2,5), white(3,5), black(4,5), white(5,5).
valid_col5_5 :- white(1,5), white(2,5), white(3,5), white(4,5), black(5,5).

% Ensure at least one valid configuration for each row
:- row_clue(1, 2, 1), not valid_row1_1, not valid_row1_2, not valid_row1_3, not valid_row1_4.
:- row_clue(2, 1, 1), not valid_row2_1, not valid_row2_2, not valid_row2_3, not valid_row2_4, not valid_row2_5.
:- row_clue(3, 3, 1), not valid_row3_1, not valid_row3_2, not valid_row3_3.
:- row_clue(4, 1, 1), not valid_row4_1, not valid_row4_2, not valid_row4_3, not valid_row4_4, not valid_row4_5, not valid_row4_6.
:- row_clue(5, 2, 1), not valid_row5_1, not valid_row5_2, not valid_row5_3, not valid_row5_4.

% Ensure at least one valid configuration for each column
:- col_clue(1, 1, 1), not valid_col1_1, not valid_col1_2, not valid_col1_3, not valid_col1_4, not valid_col1_5, not valid_col1_6.
:- col_clue(2, 1, 1), not valid_col2_1, not valid_col2_2.
:- col_clue(2, 3, 2), not valid_col2_1, not valid_col2_2.
:- col_clue(3, 2, 1), not valid_col3_1, not valid_col3_2, not valid_col3_3, not valid_col3_4.
:- col_clue(4, 1, 1), not valid_col4_1, not valid_col4_2, not valid_col4_3, not valid_col4_4, not valid_col4_5.
:- col_clue(5, 1, 1), not valid_col5_1, not valid_col5_2, not valid_col5_3, not valid_col5_4, not valid_col5_5.

% Show the grid values
#show value/3.