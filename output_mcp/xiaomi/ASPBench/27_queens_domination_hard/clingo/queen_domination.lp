% Queen Domination Problem on 9x9 Board
% Find minimum number of queens to dominate all squares

% Board dimensions
#const n = 9.
row(0..n-1).
col(0..n-1).

% A square is a pair (R, C)
square(R, C) :- row(R), col(C).

% Decision: place a queen on a square (choice rule)
{ queen(R, C) } :- square(R, C).

% Domination rules
% A queen dominates its own row
dominates(R, C, R, C2) :- queen(R, C), col(C2).

% A queen dominates its own column
dominates(R, C, R2, C) :- queen(R, C), row(R2).

% A queen dominates its diagonals
% Diagonal: same difference (R - C)
dominates(R, C, R2, C2) :- queen(R, C), square(R2, C2), R - C == R2 - C2.

% Anti-diagonal: same sum (R + C)
dominates(R, C, R2, C2) :- queen(R, C), square(R2, C2), R + C == R2 + C2.

% A square is dominated if any queen dominates it
dominated(R, C) :- dominates(_, _, R, C).

% Constraint: every square must be dominated
:- square(R, C), not dominated(R, C).

% Count queens
queen_count(N) :- N = #count { R, C : queen(R, C) }.

% Minimize number of queens
#minimize { 1, R, C : queen(R, C) }.

% Show results
#show queen/2.
#show queen_count/1.