% Protein folding problem using HP model
% Sequence: HPPHPPHH (8 residues)

% Sequence data
residue(1..8).
sequence(1,"H").
sequence(2,"P").
sequence(3,"P").
sequence(4,"H").
sequence(5,"P").
sequence(6,"P").
sequence(7,"H").
sequence(8,"H").

% Lattice bounds (reasonable for 8 residues)
x(-5..5).
y(-5..5).

% Assign coordinates to residues (choice rule)
{ coordinate(R, X, Y) : x(X), y(Y) } = 1 :- residue(R).

% Ensure all residues are placed
:- residue(R), not coordinate(R, _, _).

% Consecutive residues must be adjacent (Manhattan distance = 1)
:- residue(R), residue(R+1),
   coordinate(R, X1, Y1), coordinate(R+1, X2, Y2),
   |X1 - X2| + |Y1 - Y2| != 1.

% All coordinates must be unique (self-avoiding walk)
:- coordinate(R1, X, Y), coordinate(R2, X, Y), R1 != R2.

% Calculate contacts between non-sequential neighbors
% Two residues are in contact if they are adjacent but not consecutive
contact(R1, R2) :-
    residue(R1), residue(R2),
    R1 < R2 - 1,  % Non-sequential
    coordinate(R1, X1, Y1),
    coordinate(R2, X2, Y2),
    |X1 - X2| + |Y1 - Y2| = 1.

% Count H-H contacts (only between non-sequential neighbors)
hh_contact(R1, R2) :- contact(R1, R2), sequence(R1, "H"), sequence(R2, "H").

% Minimize energy by maximizing H-H contacts
% Each H-H contact contributes -1 to energy
#minimize { -1 : hh_contact(R1, R2) }.

% Show the solution
#show coordinate/3.
#show energy/1.

% Calculate and show energy for verification
num_hh_contacts(N) :- N = #count { R1, R2 : hh_contact(R1, R2) }.
energy(E) :- E = -N, num_hh_contacts(N).
#show energy/1.