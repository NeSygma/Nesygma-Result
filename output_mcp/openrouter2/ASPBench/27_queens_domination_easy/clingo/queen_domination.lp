% Domain
row(0..7).
col(0..7).
square(R,C) :- row(R), col(C).

% Choice of queens
{ queen(R,C) } :- square(R,C).

% Dominated squares
% Own square
ominated(R,C) :- queen(R,C).
% Same row
ominated(R,C) :- queen(R1,C1), R1 = R, col(C).
% Same column
ominated(R,C) :- queen(R1,C1), C1 = C, row(R).
% Main diagonal
ominated(R,C) :- queen(R1,C1), R1 - R = C1 - C, row(R), col(C).
% Anti-diagonal
ominated(R,C) :- queen(R1,C1), R1 - R = -(C1 - C), row(R), col(C).

% All squares must be dominated
:- square(R,C), not dominated(R,C).

% Count queens
num_queens(N) :- N = #count{R,C : queen(R,C)}.

% Objective: minimize number of queens
:~ queen(R,C). [1@1]

% Show
#show queen/2.
#show dominated/2.
#show num_queens/1.