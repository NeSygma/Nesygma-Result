% Domain
row(0..8).
col(0..8).

% Choice of queen positions
{ queen(R,C) } :- row(R), col(C).

% Dominated squares
% A queen dominates its own square

dominated(R,C) :- queen(R,C).
% Same row

dominated(R,C) :- queen(R1,C), R != R1, row(R).
% Same column

dominated(R,C) :- queen(R,C1), C != C1, col(C).
% Diagonals

dominated(R,C) :- queen(R1,C1), abs(R-R1) = abs(C-C1), row(R), col(C).

% All squares must be dominated
:- row(R), col(C), not dominated(R,C).

% Count queens
queen_count(N) :- N = #count{R,C : queen(R,C)}.

% Objective: minimize number of queens
#minimize {1@1, queen(R,C) : queen(R,C)}.

% Show
#show queen/2.
#show queen_count/1.