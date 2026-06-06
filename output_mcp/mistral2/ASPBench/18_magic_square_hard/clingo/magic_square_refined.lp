% --- Declare the grid and values ---
% Grid cells: 1-based indexing for rows and columns
cell(1..4, 1..4).

% Values to place: 1 to 16
value(1..16).

% Assign each number to exactly one cell
1 { value_at(R, C, N) : cell(R, C) } 1 :- value(N).
:- value_at(R, C, N1), value_at(R, C, N2), N1 != N2.

% Each number from 1 to 16 is used exactly once
:- value(N), not used(N).
used(N) :- value_at(_, _, N).

% --- Magic sum constraints ---
magic_sum(34).

% Row sums
row_sum(R) :- cell(R, _), magic_sum(S), S = #sum { N : value_at(R, C, N), cell(R, C) }.
:- cell(R, _), not row_sum(R).

% Column sums
col_sum(C) :- cell(_, C), magic_sum(S), S = #sum { N : value_at(R, C, N), cell(R, C) }.
:- cell(_, C), not col_sum(C).

% Diagonal sums (main and anti)
diag1_sum :- magic_sum(S), S = #sum { N : value_at(R, R, N), cell(R, R) }.
:- not diag1_sum.

diag2_sum :- magic_sum(S), S = #sum { N : value_at(R, 5-R, N), cell(R, 5-R) }.
:- not diag2_sum.

% --- Symmetrical pairs constraint ---
% Define opposite cells: (R, C) is opposite to (5-R, 5-C)
opposite(R, C, 5-R, 5-C) :- cell(R, C).

% Opposite cells must sum to 17
:- opposite(R1, C1, R2, C2), value_at(R1, C1, N1), value_at(R2, C2, N2), N1 + N2 != 17.

% --- Prime placement constraint ---
% Small primes
prime(2). prime(3). prime(5). prime(7).

% Corners
corner(1, 1). corner(1, 4). corner(4, 1). corner(4, 4).

% Primes cannot be in corners
:- corner(R, C), value_at(R, C, N), prime(N).

% --- Show the solution ---
#show value_at/3.