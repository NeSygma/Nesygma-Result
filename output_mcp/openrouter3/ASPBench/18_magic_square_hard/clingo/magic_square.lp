% Magic Square 4x4 Problem
% Place numbers 1-16 in a 4x4 grid with various constraints

% Domain declarations
row(1..4).
col(1..4).
value(1..16).
quadrant(1..4). % 1: TL, 2: TR, 3: BL, 4: BR

% Small primes
prime(2). prime(3). prime(5). prime(7).

% Corner cells
corner(1,1). corner(1,4). corner(4,1). corner(4,4).

% Magic constant
magic_constant(34).

% Choice rule: assign exactly one value to each cell
{ value(R, C, V) : value(V) } 1 :- row(R), col(C).

% Constraint: each value used exactly once
:- value(_, _, V), #count{R, C : value(R, C, V)} != 1.

% Row sums
row_sum(R, S) :- row(R), S = #sum{V, C : value(R, C, V), col(C)}.
:- row_sum(R, S), magic_constant(M), S != M.

% Column sums  
col_sum(C, S) :- col(C), S = #sum{V, R : value(R, C, V), row(R)}.
:- col_sum(C, S), magic_constant(M), S != M.

% Diagonal sums
% Main diagonal: (1,1), (2,2), (3,3), (4,4)
diag_sum(1, S) :- S = #sum{V, R : value(R, R, V), row(R)}.
% Anti-diagonal: (1,4), (2,3), (3,2), (4,1)
diag_sum(2, S) :- S = #sum{V, R : value(R, 5-R, V), row(R)}.
:- diag_sum(D, S), magic_constant(M), S != M.

% Opposite cells sum to 17
% (r,c) opposite is (5-r, 5-c)
opposite_sum(R, C, S) :- row(R), col(C), 
    S = #sum{V1+V2 : value(R, C, V1), value(5-R, 5-C, V2)}.
:- opposite_sum(R, C, S), S != 17.

% Quadrant definitions and sums
% Quadrant 1 (TL): rows 1-2, cols 1-2
quadrant_sum(1, S) :- S = #sum{V, R, C : value(R, C, V), R <= 2, C <= 2}.
% Quadrant 2 (TR): rows 1-2, cols 3-4  
quadrant_sum(2, S) :- S = #sum{V, R, C : value(R, C, V), R <= 2, C >= 3}.
% Quadrant 3 (BL): rows 3-4, cols 1-2
quadrant_sum(3, S) :- S = #sum{V, R, C : value(R, C, V), R >= 3, C <= 2}.
% Quadrant 4 (BR): rows 3-4, cols 3-4
quadrant_sum(4, S) :- S = #sum{V, R, C : value(R, C, V), R >= 3, C >= 3}.
:- quadrant_sum(Q, S), magic_constant(M), S != M.

% Prime placement constraint: no primes in corners
:- corner(R, C), value(R, C, V), prime(V).

% Show the solution
#show value/3.
#show row_sum/2.
#show col_sum/2.
#show diag_sum/2.
#show quadrant_sum/2.