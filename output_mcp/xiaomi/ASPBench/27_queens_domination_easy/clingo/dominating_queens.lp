% ===== Domain =====
row(0..7).
col(0..7).
square(R, C) :- row(R), col(C).

% ===== Choice: Place queens =====
{ queen(R, C) } :- square(R, C).

% ===== Dominance Relations =====
% A queen dominates its own row
same_row(R, C1, R, C2) :- row(R), col(C1), col(C2).

% A queen dominates its own column
same_col(R1, C, R2, C) :- col(C), row(R1), row(R2).

% A queen dominates both diagonals
% Main diagonal: R1 - C1 == R2 - C2  =>  R1 - R2 == C1 - C2
same_diag(R1, C1, R2, C2) :- square(R1, C1), square(R2, C2), 
                              R1 - R2 == C1 - C2.
% Anti-diagonal: R1 + C1 == R2 + C2
same_diag(R1, C1, R2, C2) :- square(R1, C1), square(R2, C2), 
                              R1 + C2 == R2 + C1.

% ===== Dominated Squares =====
% A square is dominated if there exists a queen that can attack it
dominated(R, C) :- square(R, C), queen(QR, QC), same_row(QR, QC, R, C).
dominated(R, C) :- square(R, C), queen(QR, QC), same_col(QR, QC, R, C).
dominated(R, C) :- square(R, C), queen(QR, QC), same_diag(QR, QC, R, C).

% ===== Constraint: All squares must be dominated =====
:- square(R, C), not dominated(R, C).

% ===== Optimization: Minimize number of queens =====
#minimize { 1, R, C : queen(R, C) }.

% ===== Output =====
#show queen/2.
#show num_queens/1.
#show dominated/2.

num_queens(N) :- N = #count { R, C : queen(R, C) }.