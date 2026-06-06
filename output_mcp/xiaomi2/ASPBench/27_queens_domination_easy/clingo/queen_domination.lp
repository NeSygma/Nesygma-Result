% Queen Domination Problem on 8x8 Chessboard
% Find minimum number of queens to dominate all squares

% Board definition
row(0..7).
col(0..7).

% A square exists on the board
square(R, C) :- row(R), col(C).

% Choice: place a queen on each square (or not)
{ queen(R, C) } :- square(R, C).

% A square is dominated if it shares a row with a queen
dominated(R, C) :- queen(R, _), square(R, C).

% A square is dominated if it shares a column with a queen
dominated(R, C) :- queen(_, C), square(R, C).

% A square is dominated if it shares a diagonal with a queen
% Diagonal 1: R - C = RQ - CQ  =>  R - RQ = C - CQ
dominated(R, C) :- queen(RQ, CQ), square(R, C), R - RQ = C - CQ.

% Diagonal 2: R + C = RQ + CQ  =>  R - RQ = -(C - CQ)
dominated(R, C) :- queen(RQ, CQ), square(R, C), R - RQ = CQ - C.

% Constraint: every square must be dominated
:- square(R, C), not dominated(R, C).

% Count queens
num_queens(N) :- N = #count { R, C : queen(R, C) }.

% Minimize number of queens
#minimize { 1, R, C : queen(R, C) }.

% Output
#show queen/2.
#show num_queens/1.