% Define the board size
row(0..7).
col(0..7).
square(R, C) :- row(R), col(C).

% Choice rule: place queens on the board
{ queen(R, C) : square(R, C) }.

% Count the number of queens
num_queens(N) :- N = #count { R, C : queen(R, C) }.

% A queen at (R, C) dominates:
% 1. All squares in row R
% 2. All squares in column C
% 3. All squares on the two diagonals through (R, C)
dominated(R, C) :-
    queen(R0, C0),
    square(R, C),
    (R = R0 ; C = C0 ; R - C = R0 - C0 ; R + C = R0 + C0).

% All squares must be dominated
:- square(R, C), not dominated(R, C).

% Objective: minimize the number of queens
#minimize { 1@1, R, C : queen(R, C) }.

% Show the number of queens and the dominated squares
#show num_queens/1.
#show queen/2.
#show dominated/2.