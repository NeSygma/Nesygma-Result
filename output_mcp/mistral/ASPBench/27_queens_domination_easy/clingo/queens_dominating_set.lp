% Define the board
pos(0..7).

% Choice rule for placing queens
{ queen(R, C) : pos(R), pos(C) }.

% A square (R, C) is dominated if there's a queen in the same row, column, or diagonal
dominated(R, C) :-
    queen(R, _), pos(R), pos(C).  % Queen in same row

dominated(R, C) :-
    queen(_, C), pos(R), pos(C).  % Queen in same column

dominated(R, C) :-
    queen(R1, C1), R1 - C1 = R - C, pos(R), pos(C), pos(R1), pos(C1).  % Queen on same main diagonal

dominated(R, C) :-
    queen(R1, C1), R1 + C1 = R + C, pos(R), pos(C), pos(R1), pos(C1).  % Queen on same anti-diagonal

% All squares must be dominated
:- pos(R), pos(C), not dominated(R, C).

% Minimize the number of queens
#minimize { 1@1 : queen(R, C) }.

% Show the queens and dominated squares
#show queen/2.
#show dominated/2.