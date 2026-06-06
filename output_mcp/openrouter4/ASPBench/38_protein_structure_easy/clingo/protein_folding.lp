% Protein Folding: HP model for sequence HPPHPPHH (8 residues)
% Minimize energy by maximizing H-H contacts between non-sequential neighbors

% --- Domain Definitions ---
residue(0..7).

% Hydrophobic residues (H) at positions: 0, 3, 6, 7
h(0). h(3). h(6). h(7).

% Coordinate range - enough room for 8 residues
coord(0..7).

% --- Placement ---
% Fix residue 0 at origin to break translational symmetry
pos(0, 0, 0).

% Fix residue 1 at (1,0) to break rotational symmetry
pos(1, 1, 0).

% Each remaining residue gets exactly one (x,y) coordinate
1 { pos(R, X, Y) : coord(X), coord(Y) } 1 :- residue(R), R > 1.

% --- Constraints ---

% 1. Consecutive residues must be adjacent (Manhattan distance = 1)
:- residue(R), R < 7, pos(R, X1, Y1), pos(R+1, X2, Y2), |X1-X2| + |Y1-Y2| != 1.

% 2. Self-avoiding walk: no two residues can occupy the same coordinate
:- residue(R1), residue(R2), R1 < R2, pos(R1, X, Y), pos(R2, X, Y).

% --- H-H Contacts (Energy Model) ---
% Two hydrophobic residues at non-sequential positions (distance > 1 in sequence)
% that are adjacent on the lattice form a contact contributing -1 energy
contact(R1, R2) :- h(R1), h(R2), R1 < R2, R2 - R1 > 1,
                   pos(R1, X1, Y1), pos(R2, X2, Y2),
                   |X1-X2| + |Y1-Y2| = 1.

% --- Optimization ---
% Maximize number of H-H contacts (minimizes energy since each contact = -1)
#maximize { 1@1, R1, R2 : contact(R1, R2) }.

% --- Output ---
% Compute energy and contact count
contact_count(N) :- N = #count { R1, R2 : contact(R1, R2) }.
energy(E) :- contact_count(N), E = -N.

% Show results
#show pos/3.
#show contact/2.
#show contact_count/1.
#show energy/1.