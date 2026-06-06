% Board dimensions
row(0..8).
col(0..8).
square(R, C) :- row(R), col(C).

% Each square may have a queen
{ queen(R, C) } :- square(R, C).

% Domination rules: a square is dominated if there exists a queen in the same row, column, or diagonal
dominated(R, C) :- queen(R, C).  % queen dominates itself
dominated(R, C) :- queen(Rq, C), row(R), col(C), row(Rq).  % same column
dominated(R, C) :- queen(R, Cq), row(R), col(C), col(Cq).  % same row
dominated(R, C) :- queen(Rq, Cq), square(R, C), R - C == Rq - Cq.  % same main diagonal (\) 
dominated(R, C) :- queen(Rq, Cq), square(R, C), R + C == Rq + Cq.  % same anti-diagonal (/)

% Constraint: every square must be dominated
:- square(R, C), not dominated(R, C).

% Minimize the number of queens
#minimize { 1, R, C : queen(R, C) }.

% Show the result
#show queen/2.