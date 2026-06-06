% Domain
row(0..7).
col(0..7).
square(R, C) :- row(R), col(C).

% Choose queens (we want to minimize the count)
{ queen(R, C) : square(R, C) }.

% A queen dominates squares in same row
dominates(R, C, R2, C2) :- queen(R, C), square(R2, C2), R = R2.

% A queen dominates squares in same column
dominates(R, C, R2, C2) :- queen(R, C), square(R2, C2), C = C2.

% A queen dominates squares on same main diagonal (r-c constant)
dominates(R, C, R2, C2) :- queen(R, C), square(R2, C2), R - C = R2 - C2.

% A queen dominates squares on same anti-diagonal (r+c constant)
dominates(R, C, R2, C2) :- queen(R, C), square(R2, C2), R + C = R2 + C2.

% A square is dominated if at least one queen dominates it
dominated(R, C) :- square(R, C), dominates(_, _, R, C).

% All squares must be dominated
:- square(R, C), not dominated(R, C).

% Minimize number of queens
#minimize { 1@1, R, C : queen(R, C) }.

% Show results
#show queen/2.