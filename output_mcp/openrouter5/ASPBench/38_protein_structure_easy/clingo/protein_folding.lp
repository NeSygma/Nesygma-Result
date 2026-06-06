% Protein Folding: HP model on 2D lattice
% Sequence: HPPHPPHH (8 residues)

% Define the sequence
residue(1, h).  % H
residue(2, p).  % P
residue(3, p).  % P
residue(4, h).  % H
residue(5, p).  % P
residue(6, p).  % P
residue(7, h).  % H
residue(8, h).  % H

% Define the 8 residues
res(1..8).

% Define lattice bounds - we need enough space for 8 residues
% A 4x4 grid (coordinates 0..3) is sufficient for a self-avoiding walk of length 8
coord(0..3).

% Each residue gets exactly one (x,y) coordinate
1 { pos(R, X, Y) : coord(X), coord(Y) } 1 :- res(R).

% Constraint 4: No two residues can occupy the same coordinate
:- pos(R1, X, Y), pos(R2, X, Y), R1 != R2.

% Constraint 2: Consecutive residues must be adjacent (Manhattan distance = 1)
:- pos(R, X1, Y1), pos(R+1, X2, Y2), |X1-X2| + |Y1-Y2| != 1.

% Define adjacency for non-sequential neighbors
% Two residues are adjacent on the lattice if Manhattan distance = 1
adjacent(R1, R2) :- pos(R1, X1, Y1), pos(R2, X2, Y2), R1 != R2, |X1-X2| + |Y1-Y2| = 1.

% H-H contact: adjacent non-sequential neighbors that are both H
% Non-sequential means |R1 - R2| > 1
hh_contact(R1, R2) :- adjacent(R1, R2), residue(R1, h), residue(R2, h), |R1-R2| > 1.

% Count total H-H contacts (each pair counted once via R1 < R2)
total_hh_contacts(N) :- N = #count { R1, R2 : hh_contact(R1, R2), R1 < R2 }.

% Energy = -1 per H-H contact
energy(E) :- total_hh_contacts(N), E = -N.

% Minimize energy (maximize |energy|)
#minimize { E : energy(E) }.

% Show results
#show pos/3.
#show hh_contact/2.
#show total_hh_contacts/1.
#show energy/1.