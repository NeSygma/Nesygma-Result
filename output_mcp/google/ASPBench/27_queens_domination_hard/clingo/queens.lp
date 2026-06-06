% Board dimensions
row(0..8).
col(0..8).

% Choice rule: place a queen at any square
{ queen(R, C) } :- row(R), col(C).

% A square is dominated if:
% 1. There is a queen on it
% 2. There is a queen in the same row
% 3. There is a queen in the same column
% 4. There is a queen on the same main diagonal (R-C = constant)
% 5. There is a queen on the same anti-diagonal (R+C = constant)

dominated(R, C) :- queen(R, C).
dominated(R, C) :- row(R), col(C), queen(QR, C), row(QR).
dominated(R, C) :- row(R), col(C), queen(R, QC), col(QC).
dominated(R, C) :- row(R), col(C), queen(QR, QC), row(QR), col(QC), R-C == QR-QC.
dominated(R, C) :- row(R), col(C), queen(QR, QC), row(QR), col(QC), R+C == QR+QC.

% Constraint: All squares must be dominated
:- row(R), col(C), not dominated(R, C).

% Objective: Minimize the number of queens
#minimize { 1, R, C : queen(R, C) }.

% Output the queen positions
#show queen/2.