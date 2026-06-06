% Nonogram 5x5 puzzle

% Domain
row(1..5).
col(1..5).

% Define black cells as a choice
{ black(R,C) } :- row(R), col(C).

% Row constraints
% Row 1: exactly two black cells, consecutive
:- #count{C : black(1,C), col(C)} != 2.
:- black(1,C), black(1,D), C < D, D - C > 1.

% Row 2: exactly one black cell
:- #count{C : black(2,C), col(C)} != 1.

% Row 3: exactly three black cells, consecutive
:- #count{C : black(3,C), col(C)} != 3.
:- black(3,C), black(3,D), C < D, D - C > 2.

% Row 4: exactly two black cells, not adjacent
:- #count{C : black(4,C), col(C)} != 2.
:- black(4,C), black(4,D), C < D, D - C = 1.

% Row 5: exactly two black cells, consecutive
:- #count{C : black(5,C), col(C)} != 2.
:- black(5,C), black(5,D), C < D, D - C > 1.

% Column constraints
% Col 1: exactly two black cells, not adjacent
:- #count{R : black(R,1), row(R)} != 2.
:- black(R1,1), black(R2,1), R1 < R2, R2 - R1 = 1.

% Col 2: exactly four black cells, with pattern: one black, then at least one white, then three consecutive blacks.
:- #count{R : black(R,2), row(R)} != 4.
% The white row must be either row1 or row2.
{ white_at_row1, white_at_row2 } 1 :- col(2).
% If white at row1, then black at rows 2,3,4,5.
black(2,2) :- white_at_row1.
black(3,2) :- white_at_row1.
black(4,2) :- white_at_row1.
black(5,2) :- white_at_row1.
% If white at row2, then black at rows 1,3,4,5.
black(1,2) :- white_at_row2.
black(3,2) :- white_at_row2.
black(4,2) :- white_at_row2.
black(5,2) :- white_at_row2.
% Forbid black at the white row.
:- white_at_row1, black(1,2).
:- white_at_row2, black(2,2).

% Col 3: exactly two black cells, consecutive
:- #count{R : black(R,3), row(R)} != 2.
:- black(R1,3), black(R2,3), R1 < R2, R2 - R1 > 1.

% Col 4: exactly one black cell
:- #count{R : black(R,4), row(R)} != 1.

% Col 5: exactly one black cell
:- #count{R : black(R,5), row(R)} != 1.

% Show the grid
#show black/2.