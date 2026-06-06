% Queens Domination Problem
% Find minimum number of queens to dominate all squares on 8x8 board

% Domain: squares
square(0..7, 0..7).

% Choice rule: place a queen on any square (at most one per square)
{ queen(R, C) } :- square(R, C).

% Domination rules: a queen dominates its row, column, and both diagonals
% We need to enumerate all squares to ground R and C
dominated(R, C) :- queen(R0, C0), square(R, C), R = R0.
dominated(R, C) :- queen(R0, C0), square(R, C), C = C0.
dominated(R, C) :- queen(R0, C0), square(R, C), R - C = R0 - C0.
dominated(R, C) :- queen(R0, C0), square(R, C), R + C = R0 + C0.

% All squares must be dominated
:- not dominated(R, C), square(R, C).

% Count number of queens
num_queens(N) :- N = #count { R, C : queen(R, C) }.

% Minimize number of queens
#minimize { 1, R, C : queen(R, C) }.

% Output: queen positions, number of queens, and dominated squares (all squares)
#show queen/2.
#show num_queens/1.
#show dominated_squares/2.
dominated_squares(R, C) :- square(R, C).