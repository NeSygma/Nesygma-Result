% Define the board size
row(0..8).
col(0..8).

% Define all squares on the board
square(R, C) :- row(R), col(C).

% Choice rule: place queens on the board
{ queen(R, C) : row(R), col(C) }.

% Define dominating conditions for each square
% Same row
dominated(R, C) :- queen(R, C1), square(R, C).
% Same column
dominated(R, C) :- queen(R1, C), square(R, C).

% Diagonal: down-right (R+D, C+D)
dominated(R, C) :- queen(R1, C1), square(R, C), R - R1 = C - C1, R >= R1, C >= C1.
% Diagonal: down-left (R+D, C-D)
dominated(R, C) :- queen(R1, C1), square(R, C), R - R1 = C1 - C, R >= R1, C1 >= C.
% Diagonal: up-right (R-D, C+D)
dominated(R, C) :- queen(R1, C1), square(R, C), R1 - R = C - C1, R1 >= R, C >= C1.
% Diagonal: up-left (R-D, C-D)
dominated(R, C) :- queen(R1, C1), square(R, C), R1 - R = C1 - C, R1 >= R, C1 >= C.

% Ensure every square is dominated
:- square(R, C), not dominated(R, C).

% Minimize the number of queens
#minimize { 1@1 : queen(R, C) }.

% Show the queens in the output
#show queen/2.