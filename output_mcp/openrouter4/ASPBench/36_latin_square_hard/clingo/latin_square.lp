% Domains
row(1..8).
col(1..8).
val(1..8).

% Even and odd value classification
even_val(2;4;6;8).
odd_val(1;3;5;7).

% Each cell gets exactly one value from 1 to 8
1 { cell(R,C,V) : val(V) } 1 :- row(R), col(C).

% Latin square: each value appears exactly once per row
:- row(R), val(V), #count { C : cell(R,C,V) } != 1.

% Latin square: each value appears exactly once per column
:- col(C), val(V), #count { R : cell(R,C,V) } != 1.

% Pre-filled cells
cell(1,1,1).
cell(1,8,8).
cell(2,2,6).
cell(3,3,4).
cell(4,4,5).
cell(5,5,7).
cell(6,6,4).
cell(7,7,6).
cell(8,8,3).
cell(8,1,8).

% Adjacent pair sum constraint: every horizontally adjacent pair must sum > 5
:- row(R), col(C), C < 8, cell(R,C,V1), cell(R,C+1,V2), V1 + V2 <= 5.

% Quadrant parity constraints
% Top-left quadrant (rows 1-4, cols 1-4) must have exactly 8 even numbers
:- #count { R,C : row(R), col(C), R <= 4, C <= 4, cell(R,C,V), even_val(V) } != 8.

% Bottom-right quadrant (rows 5-8, cols 5-8) must have exactly 8 odd numbers
:- #count { R,C : row(R), col(C), R >= 5, C >= 5, cell(R,C,V), odd_val(V) } != 8.

% Partial sum constraints
% Sum of first four cells in row 1 = 14
:- #sum { V, C : col(C), C <= 4, cell(1,C,V) } != 14.

% Sum of first four cells in column 1 = 10
:- #sum { V, R : row(R), R <= 4, cell(R,1,V) } != 10.

% Show result
#show cell/3.