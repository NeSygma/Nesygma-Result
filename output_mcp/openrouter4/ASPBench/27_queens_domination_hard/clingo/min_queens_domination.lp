% Domain
row(0..8).
col(0..8).
square(R,C) :- row(R), col(C).

% Choice: place a queen at any square
{ queen(R,C) : row(R), col(C) }.

% Domination rules
% A queen dominates itself
dominated(R,C) :- queen(R,C).

% Same column: queen at (Rq, C) dominates all (R, C)
dominated(R,C) :- queen(Rq, C), square(R,C).

% Same row: queen at (R, Cq) dominates all (R, C)
dominated(R,C) :- queen(R, Cq), square(R,C).

% Same diagonal (/): R+C constant
dominated(R,C) :- queen(Rq, Cq), square(R,C), R + C == Rq + Cq.

% Same diagonal (\: R-C constant)
dominated(R,C) :- queen(Rq, Cq), square(R,C), R - C == Rq - Cq.

% Constraint: all squares must be dominated
:- square(R,C), not dominated(R,C).

% Minimize number of queens
#minimize { 1,R,C : queen(R,C) }.

% Show results
#show queen/2.