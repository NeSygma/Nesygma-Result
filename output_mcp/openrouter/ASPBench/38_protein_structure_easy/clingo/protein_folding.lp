% Domain of coordinates
x(-7..7).
y(-7..7).

% Residues
residue(1..8).

% Sequence definition
seq(1,"H").
seq(2,"P").
seq(3,"P").
seq(4,"H").
seq(5,"P").
seq(6,"P").
seq(7,"H").
seq(8,"H").

% Hydrophobic predicate
hydrophobic(I) :- seq(I,"H").

% Assign exactly one coordinate to each residue
1 { coord(I,X,Y) : x(X), y(Y) } 1 :- residue(I).

% Uniqueness: no two residues share a coordinate
:- coord(I,X,Y), coord(J,X,Y), I < J.

% Consecutive residues must be adjacent (Manhattan distance 1)
:- residue(I), J = I+1, coord(I,X1,Y1), coord(J,X2,Y2), D = abs(X1-X2) + abs(Y1-Y2), D != 1.

% Define consecutive relation for convenience
consecutive(I,J) :- residue(I), J = I+1.

% H-H contacts between non‑sequential neighbors (Manhattan distance 1)
contact(I,J) :- hydrophobic(I), hydrophobic(J), I < J, not consecutive(I,J),
                coord(I,X1,Y1), coord(J,X2,Y2),
                D = abs(X1-X2) + abs(Y1-Y2), D = 1.

% Objective: maximize number of H‑H contacts
#maximize { 1, I, J : contact(I,J) }.

% Tie‑breaking: lexicographically minimise coordinates (first X then Y)
#minimize { X, I : coord(I,X,_) }.
#minimize { Y, I : coord(I,_,Y) }.

#show coord/3.