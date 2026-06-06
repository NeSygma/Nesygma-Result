% Protein sequence: HPPHPPHH (8 residues)
residue(1..8).

% Residue types
type(1, h). type(2, p). type(3, p). type(4, h).
type(5, p). type(6, p). type(7, h). type(8, h).

% Coordinate bounds - need enough space for 8 residues
% Use range -7..7 to allow flexibility
x(-7..7). y(-7..7).

% Each residue gets exactly one coordinate
1 { coord(I, X, Y) : x(X), y(Y) } 1 :- residue(I).

% Constraint: No two residues on same coordinate
:- coord(I1, X, Y), coord(I2, X, Y), I1 < I2.

% Constraint: Consecutive residues must be adjacent (Manhattan distance = 1)
:- coord(I, X1, Y1), coord(I+1, X2, Y2), 
   |X1 - X2| + |Y1 - Y2| != 1.

% Define non-sequential adjacency (lattice neighbors, not sequence neighbors)
% Two residues are lattice neighbors if Manhattan distance = 1
lattice_neighbor(I, J) :- coord(I, X1, Y1), coord(J, X2, Y2), 
                          |X1 - X2| + |Y1 - Y2| = 1, I != J.

% Non-sequential means |I - J| > 1
non_sequential(I, J) :- residue(I), residue(J), I < J, J > I + 1.

% H-H contact: both are hydrophobic and non-sequential lattice neighbors
hh_contact(I, J) :- lattice_neighbor(I, J), non_sequential(I, J),
                     type(I, h), type(J, h).

% Count H-H contacts
contact_count(N) :- N = #count{I, J : hh_contact(I, J)}.

% Energy is negative of contact count (each contact gives -1)
energy(E) :- contact_count(N), E = -N.

% Minimize energy (maximize contacts)
#minimize { E, E : energy(E) }.

% Show coordinates in sequence order
#show coord/3.
#show energy/1.