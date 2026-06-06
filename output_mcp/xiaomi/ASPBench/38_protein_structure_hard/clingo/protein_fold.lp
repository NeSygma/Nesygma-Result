% Protein Folding on 2D Lattice - HP Model
% Sequence: HPHPHHPHPH (10 residues)

% ============ DOMAIN DEFINITIONS ============

% Residue positions (1-indexed)
residue(1..10).

% Residue types
h(1). p(2). h(3). p(4). h(5). h(6). p(7). h(8). p(9). h(10).

% Lattice coordinates - bounded to reduce search space
% For 10 residues, we need at most a 10x10 grid, but we can bound tighter
coord(-5..5).

% ============ CHOICE RULES ============

% Assign each residue to exactly one (x,y) coordinate
{ at(R, X, Y) : coord(X), coord(Y) } 1 :- residue(R).

% ============ CONSTRAINTS ============

% Self-avoiding walk: no two residues at the same position
:- at(R1, X, Y), at(R2, X, Y), R1 < R2.

% Connectivity: consecutive residues must be adjacent (Manhattan distance = 1)
% |x1-x2| + |y1-y2| = 1
adjacent(R, R+1) :- residue(R), R < 10, 
                     at(R, X1, Y1), at(R+1, X2, Y2),
                     D = |X1-X2| + |Y1-Y2|, D = 1.

% Enforce adjacency for consecutive residues
:- residue(R), R < 10, not adjacent(R, R+1).

% ============ ENERGY CALCULATION ============

% Count non-sequential H-H contacts
% Two H residues at adjacent lattice points with |i-j| > 1
contact(R1, R2) :- h(R1), h(R2), R1 < R2, R2 > R1 + 1,
                    at(R1, X1, Y1), at(R2, X2, Y2),
                    D = |X1-X2| + |Y1-Y2|, D = 1.

% Total energy is negative of contact count
energy(N) :- N = #count{ R1, R2 : contact(R1, R2) }.

% ============ OPTIMIZATION ============

% Minimize energy (maximize contacts since energy = -contacts)
#maximize { N, E : energy(E), N = E }.

% ============ OUTPUT ============

#show at/3.
#show energy/1.