% Define the grid size
row(1..8).
col(1..8).
value(1..8).

% Pre-filled cells (1-indexed)
prefilled(1,1,1).
prefilled(1,8,8).
prefilled(2,2,6).
prefilled(3,3,4).
prefilled(4,4,5).
prefilled(5,5,7).
prefilled(6,6,4).
prefilled(7,7,6).
prefilled(8,8,3).
prefilled(8,1,8).

% Define quadrants
% Top-left: rows 1-4, cols 1-4
in_top_left(R,C) :- row(R), col(C), R <= 4, C <= 4.
% Bottom-right: rows 5-8, cols 5-8
in_bottom_right(R,C) :- row(R), col(C), R >= 5, C >= 5.

% Define even and odd values
even(2).
even(4).
even(6).
even(8).
odd(1).
odd(3).
odd(5).
odd(7).

% Latin square: each cell has exactly one value
1 { cell(R, C, V) : value(V) } 1 :- row(R), col(C).

% Prefilled cells must match
:- prefilled(R, C, V), not cell(R, C, V).
:- cell(R, C, V), prefilled(R, C, W), V != W.

% Each row contains each value exactly once
:- row(R), value(V), #count { C : cell(R, C, V) } != 1.

% Each column contains each value exactly once
:- col(C), value(V), #count { R : cell(R, C, V) } != 1.

% Adjacent pair sum constraint: grid[r][c] + grid[r][c+1] > 5
:- row(R), col(C), C < 8, cell(R, C, V1), cell(R, C+1, V2), V1 + V2 <= 5.

% Quadrant parity constraints
% Top-left quadrant must contain exactly 8 even numbers
even_count_top_left(N) :- N = #count { R,C,V : in_top_left(R,C), cell(R,C,V), even(V) }.
:- even_count_top_left(N), N != 8.

% Bottom-right quadrant must contain exactly 8 odd numbers
odd_count_bottom_right(N) :- N = #count { R,C,V : in_bottom_right(R,C), cell(R,C,V), odd(V) }.
:- odd_count_bottom_right(N), N != 8.

% Partial sum constraints
% Sum of first four cells in row 1 = 14
sum_row1_first4(N) :- N = #sum { V,C : cell(1,C,V), C <= 4 }.
:- sum_row1_first4(N), N != 14.

% Sum of first four cells in column 1 = 10
sum_col1_first4(N) :- N = #sum { V,R : cell(R,1,V), R <= 4 }.
:- sum_col1_first4(N), N != 10.

% Show the solution
#show cell/3.