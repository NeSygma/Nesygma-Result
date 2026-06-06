% Queen Domination Problem on 9x9 Chessboard
% Find minimum number of queens to dominate all 81 squares

% Domain
row(0..8).
col(0..8).

% Square definition
square(R,C) :- row(R), col(C).

% Choice: place a queen on each square or not
{ queen(R,C) } :- square(R,C).

% A square is dominated if there's a queen in the same row
dominated(R,C) :- queen(R,_), square(R,C).

% A square is dominated if there's a queen in the same column
dominated(R,C) :- queen(_,C), square(R,C).

% A square is dominated if there's a queen on the same main diagonal (R-C = constant)
dominated(R,C) :- queen(RQ,CQ), square(R,C), R - C = RQ - CQ.

% A square is dominated if there's a queen on the same anti-diagonal (R+C = constant)
dominated(R,C) :- queen(RQ,CQ), square(R,C), R + C = RQ + CQ.

% All 81 squares must be dominated
:- square(R,C), not dominated(R,C).

% Minimize the number of queens placed
#minimize { 1,R,C : queen(R,C) }.

#show queen/2.