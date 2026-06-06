% Protein folding on 2D lattice using HP model
% Sequence: HPPHPPHH (8 residues)

% Residue definitions
residue(1..8).
type(1, "H"). type(2, "P"). type(3, "P"). type(4, "H").
type(5, "P"). type(6, "P"). type(7, "H"). type(8, "H").

% Coordinate domain: bounded grid
coord_value(-7..7).

% Each residue gets exactly one coordinate
1 { coord(I, X, Y) : coord_value(X), coord_value(Y) } 1 :- residue(I).

% No two residues share the same coordinate
:- coord(I, X, Y), coord(J, X, Y), I != J.

% Define adjacency by checking all possible adjacent pairs
% Two coordinates are adjacent if they differ by exactly 1 in one dimension and are equal in the other
adjacent(X1, Y1, X2, Y2) :- coord_value(X1), coord_value(Y1), 
                            coord_value(X2), coord_value(Y2),
                            X1 = X2, Y2 = Y1 + 1.
adjacent(X1, Y1, X2, Y2) :- coord_value(X1), coord_value(Y1), 
                            coord_value(X2), coord_value(Y2),
                            X1 = X2, Y2 = Y1 - 1.
adjacent(X1, Y1, X2, Y2) :- coord_value(X1), coord_value(Y1), 
                            coord_value(X2), coord_value(Y2),
                            X2 = X1 + 1, Y1 = Y2.
adjacent(X1, Y1, X2, Y2) :- coord_value(X1), coord_value(Y1), 
                            coord_value(X2), coord_value(Y2),
                            X2 = X1 - 1, Y1 = Y2.

% Consecutive residues must be adjacent
:- coord(I, X1, Y1), coord(I+1, X2, Y2), not adjacent(X1, Y1, X2, Y2).

% H-H contacts between non-sequential neighbors
contact(I, J) :- type(I, "H"), type(J, "H"), J != I + 1,
                 coord(I, X1, Y1), coord(J, X2, Y2),
                 adjacent(X1, Y1, X2, Y2).

% Count contacts
contact_count(N) :- N = #count{ I, J : contact(I, J) }.

% Energy = - (number of contacts)
energy(E) :- contact_count(N), E = -N.

% Minimize energy (i.e., maximize contacts)
#minimize { E, 0 : energy(E) }.

% Show coordinates for each residue
#show coord/3.
% Optionally show energy
#show energy/1.
#show contact_count/1.