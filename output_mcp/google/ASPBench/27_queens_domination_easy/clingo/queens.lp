% Board dimensions
row(0..7).
col(0..7).
square(R, C) :- row(R), col(C).

% Choice rule: place a queen on any square
{ queen(R, C) } :- square(R, C).

% Helper for diagonal condition
% (R - QR) == (C - QC)  => R - C == QR - QC
% (R - QR) == -(C - QC) => R + C == QR + QC
same_diagonal(R, C, QR, QC) :- square(R, C), square(QR, QC), R - C == QR - QC.
same_diagonal(R, C, QR, QC) :- square(R, C), square(QR, QC), R + C == QR + QC.

% A square (R, C) is dominated if there is a queen at (QR, QC) such that:
% 1. Same row: R == QR
% 2. Same column: C == QC
% 3. Same diagonal: same_diagonal(R, C, QR, QC)
is_dominated(R, C) :- square(R, C), queen(QR, QC), R == QR.
is_dominated(R, C) :- square(R, C), queen(QR, QC), C == QC.
is_dominated(R, C) :- square(R, C), queen(QR, QC), same_diagonal(R, C, QR, QC).

% Constraint: All squares must be dominated
:- square(R, C), not is_dominated(R, C).

% Objective: Minimize the number of queens
num_queens(N) :- N = #count { R, C : queen(R, C) }.
#minimize { N : num_queens(N) }.

% Output
#show queen/2.
#show num_queens/1.