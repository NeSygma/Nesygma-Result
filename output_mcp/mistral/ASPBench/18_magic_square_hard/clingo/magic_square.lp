% Magic Square Problem: 4x4 grid with numbers 1-16
% Constraints: magic sum 34, symmetrical pairs, quadrant sums, prime placement

% Grid positions (1-based indexing)
cell(1..4, 1..4).

% Values to place (1 through 16, each used exactly once)
value(1..16).

% Magic constant
magic_sum(34).

% Small primes that cannot be in corners
prime(2;3;5;7).

% Corner positions (1-based indexing)
corner(1,1). corner(1,4). corner(4,1). corner(4,4).

% Quadrant definitions (4 quadrants, 2x2 each)
% Quadrant 1 (Top-Left): cells (1,1), (1,2), (2,1), (2,2)
quadrant(1,1,1). quadrant(1,1,2).
quadrant(1,2,1). quadrant(1,2,2).

% Quadrant 2 (Top-Right): cells (1,3), (1,4), (2,3), (2,4)
quadrant(2,1,3). quadrant(2,1,4).
quadrant(2,2,3). quadrant(2,2,4).

% Quadrant 3 (Bottom-Left): cells (3,1), (3,2), (4,1), (4,2)
quadrant(3,3,1). quadrant(3,3,2).
quadrant(3,4,1). quadrant(3,4,2).

% Quadrant 4 (Bottom-Right): cells (3,3), (3,4), (4,3), (4,4)
quadrant(4,3,3). quadrant(4,3,4).
quadrant(4,4,3). quadrant(4,4,4).

% Each cell contains exactly one value
1 { value(R,C,V) : value(V) } 1 :- cell(R,C).

% Uniqueness: Each value appears exactly once in the grid
:- value(R1,C1,V), value(R2,C2,V), (R1 != R2 ; C1 != C2), cell(R1,C1), cell(R2,C2).

% Magic sum constraints

% Rows: each row must sum to magic_sum
row_sum(R) :- magic_sum(S), R = 1..4,
    S = #sum { V : value(R,C,V), cell(R,C) }.
:- not row_sum(1), not row_sum(2), not row_sum(3), not row_sum(4).

% Columns: each column must sum to magic_sum
col_sum(C) :- magic_sum(S), C = 1..4,
    S = #sum { V : value(R,C,V), cell(R,C) }.
:- not col_sum(1), not col_sum(2), not col_sum(3), not col_sum(4).

% Main diagonals: both must sum to magic_sum
main_diag1 :- magic_sum(S),
    S = #sum { V : value(R,R,V), cell(R,R) }.
main_diag2 :- magic_sum(S),
    S = #sum { V : value(R,5-R,V), cell(R,5-R) }.
:- not main_diag1, not main_diag2.

% Symmetrical pairs: opposite cells must sum to 17
% Cell (r,c) is opposite to cell (5-r,5-c)
:- value(R,C,V1), value(5-R,5-C,V2), V1 + V2 <> 17.

% Quadrant sums: each quadrant must sum to magic_sum
quadrant_sum(Q) :- magic_sum(S), Q = 1..4,
    S = #sum { V : value(R,C,V), quadrant(Q,R,C) }.
:- not quadrant_sum(1), not quadrant_sum(2), not quadrant_sum(3), not quadrant_sum(4).

% Prime placement: small primes cannot be in corner cells
:- value(R,C,V), prime(V), corner(R,C).

% Display the solution
#show value/3.