% Domain
residue(1..8).
type(1,h). type(2,p). type(3,p). type(4,h). type(5,p). type(6,p). type(7,h). type(8,h).
sequence("HPPHPPHH").

% Coordinate domain
% Use choice rule to assign each residue a unique coordinate
1 { coord(I, X, Y) : X = 0..7, Y = 0..7 } 1 :- residue(I).

% Uniqueness constraint
:- coord(I, X, Y), coord(J, X, Y), I != J.

% Adjacency definition
adjacent(X1,Y1,X2,Y2) :- X1 = X2, Y1 = Y2+1, Y2 <= 6.
adjacent(X1,Y1,X2,Y2) :- X1 = X2, Y1 = Y2-1, Y2 >= 1.
adjacent(X1,Y1,X2,Y2) :- X1 = X2+1, Y1 = Y2, X2 <= 6.
adjacent(X1,Y1,X2,Y2) :- X1 = X2-1, Y1 = Y2, X2 >= 1.

% Consecutive residues adjacency constraint
:- residue(I), residue(J), J = I+1, coord(I, X1, Y1), coord(J, X2, Y2), not adjacent(X1,Y1,X2,Y2).

% Contact rule for non-sequential H-H neighbors
contact(I,J) :- I < J, J != I+1, coord(I, X1, Y1), coord(J, X2, Y2), adjacent(X1,Y1,X2,Y2), type(I,h), type(J,h).

% Maximize number of contacts
#maximize {1 : contact(I,J)}.

#show coord/3.
#show sequence/1.