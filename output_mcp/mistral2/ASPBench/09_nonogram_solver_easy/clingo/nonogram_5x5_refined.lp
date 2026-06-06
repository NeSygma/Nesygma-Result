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
% Row 5: [2] -> one group of 2
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

% Encode row constraints
% For each row, ensure that the groups of black cells match the clues

% Row 1: [2] (one group of 2)
:- row_clue(1, 2, 1),
   not (black(1, 1), black(1, 2), white(1, 3), white(1, 4), white(1, 5)).
:- row_clue(1, 2, 1),
   not (white(1, 1), black(1, 2), black(1, 3), white(1, 4), white(1, 5)).
:- row_clue(1, 2, 1),
   not (white(1, 1), white(1, 2), black(1, 3), black(1, 4), white(1, 5)).
:- row_clue(1, 2, 1),
   not (white(1, 1), white(1, 2), white(1, 3), black(1, 4), black(1, 5)).

% Row 2: [1] (one group of 1)
:- row_clue(2, 1, 1),
   not (black(2, 1), white(2, 2), white(2, 3), white(2, 4), white(2, 5)).
:- row_clue(2, 1, 1),
   not (white(2, 1), black(2, 2), white(2, 3), white(2, 4), white(2, 5)).
:- row_clue(2, 1, 1),
   not (white(2, 1), white(2, 2), black(2, 3), white(2, 4), white(2, 5)).
:- row_clue(2, 1, 1),
   not (white(2, 1), white(2, 2), white(2, 3), black(2, 4), white(2, 5)).
:- row_clue(2, 1, 1),
   not (white(2, 1), white(2, 2), white(2, 3), white(2, 4), black(2, 5)).

% Row 3: [3] (one group of 3)
:- row_clue(3, 3, 1),
   not (black(3, 1), black(3, 2), black(3, 3), white(3, 4), white(3, 5)).
:- row_clue(3, 3, 1),
   not (white(3, 1), black(3, 2), black(3, 3), black(3, 4), white(3, 5)).
:- row_clue(3, 3, 1),
   not (white(3, 1), white(3, 2), black(3, 3), black(3, 4), black(3, 5)).

% Row 4: [1, 1] (two groups of 1, separated)
:- row_clue(4, 1, 1),
   not (black(4, 1), white(4, 2), black(4, 3), white(4, 4), white(4, 5)).
:- row_clue(4, 1, 1),
   not (black(4, 1), white(4, 2), white(4, 3), black(4, 4), white(4, 5)).
:- row_clue(4, 1, 1),
   not (black(4, 1), white(4, 2), white(4, 3), white(4, 4), black(4, 5)).
:- row_clue(4, 1, 1),
   not (white(4, 1), black(4, 2), white(4, 3), black(4, 4), white(4, 5)).
:- row_clue(4, 1, 1),
   not (white(4, 1), black(4, 2), white(4, 3), white(4, 4), black(4, 5)).
:- row_clue(4, 1, 1),
   not (white(4, 1), white(4, 2), black(4, 3), white(4, 4), black(4, 5)).

% Row 5: [2] (one group of 2)
:- row_clue(5, 2, 1),
   not (black(5, 1), black(5, 2), white(5, 3), white(5, 4), white(5, 5)).
:- row_clue(5, 2, 1),
   not (white(5, 1), black(5, 2), black(5, 3), white(5, 4), white(5, 5)).
:- row_clue(5, 2, 1),
   not (white(5, 1), white(5, 2), black(5, 3), black(5, 4), white(5, 5)).
:- row_clue(5, 2, 1),
   not (white(5, 1), white(5, 2), white(5, 3), black(5, 4), black(5, 5)).

% Column 1: [1, 1] (two groups of 1, separated)
:- col_clue(1, 1, 1),
   not (black(1, 1), white(2, 1), black(3, 1), white(4, 1), white(5, 1)).
:- col_clue(1, 1, 1),
   not (black(1, 1), white(2, 1), white(3, 1), black(4, 1), white(5, 1)).
:- col_clue(1, 1, 1),
   not (black(1, 1), white(2, 1), white(3, 1), white(4, 1), black(5, 1)).
:- col_clue(1, 1, 1),
   not (white(1, 1), black(2, 1), white(3, 1), black(4, 1), white(5, 1)).
:- col_clue(1, 1, 1),
   not (white(1, 1), black(2, 1), white(3, 1), white(4, 1), black(5, 1)).
:- col_clue(1, 1, 1),
   not (white(1, 1), white(2, 1), black(3, 1), white(4, 1), black(5, 1)).

% Column 2: [1, 3] (one group of 1, then one group of 3)
:- col_clue(2, 1, 1),
   not (black(1, 2), white(2, 2), black(3, 2), black(4, 2), black(5, 2)).
:- col_clue(2, 3, 2),
   not (white(1, 2), black(2, 2), black(3, 2), black(4, 2), white(5, 2)).

% Column 3: [2] (one group of 2)
:- col_clue(3, 2, 1),
   not (black(1, 3), black(2, 3), white(3, 3), white(4, 3), white(5, 3)).
:- col_clue(3, 2, 1),
   not (white(1, 3), black(2, 3), black(3, 3), white(4, 3), white(5, 3)).
:- col_clue(3, 2, 1),
   not (white(1, 3), white(2, 3), black(3, 3), black(4, 3), white(5, 3)).
:- col_clue(3, 2, 1),
   not (white(1, 3), white(2, 3), white(3, 3), black(4, 3), black(5, 3)).

% Column 4: [1] (one group of 1)
:- col_clue(4, 1, 1),
   not (black(1, 4), white(2, 4), white(3, 4), white(4, 4), white(5, 4)).
:- col_clue(4, 1, 1),
   not (white(1, 4), black(2, 4), white(3, 4), white(4, 4), white(5, 4)).
:- col_clue(4, 1, 1),
   not (white(1, 4), white(2, 4), black(3, 4), white(4, 4), white(5, 4)).
:- col_clue(4, 1, 1),
   not (white(1, 4), white(2, 4), white(3, 4), black(4, 4), white(5, 4)).
:- col_clue(4, 1, 1),
   not (white(1, 4), white(2, 4), white(3, 4), white(4, 4), black(5, 4)).

% Column 5: [1] (one group of 1)
:- col_clue(5, 1, 1),
   not (black(1, 5), white(2, 5), white(3, 5), white(4, 5), white(5, 5)).
:- col_clue(5, 1, 1),
   not (white(1, 5), black(2, 5), white(3, 5), white(4, 5), white(5, 5)).
:- col_clue(5, 1, 1),
   not (white(1, 5), white(2, 5), black(3, 5), white(4, 5), white(5, 5)).
:- col_clue(5, 1, 1),
   not (white(1, 5), white(2, 5), white(3, 5), black(4, 5), white(5, 5)).
:- col_clue(5, 1, 1),
   not (white(1, 5), white(2, 5), white(3, 5), white(4, 5), black(5, 5)).

% Show the grid values
#show value/3.