% Protein Folding: HP model on 2D lattice
% Sequence: HPHPHHPHPH (10 residues)
% Minimize energy = -(number of non-sequential H-H contacts)

% --- Domain ---
residue(1..10).

% Residue types
residue_type(1, h). residue_type(2, p). residue_type(3, h).
residue_type(4, p). residue_type(5, h). residue_type(6, h).
residue_type(7, p). residue_type(8, h). residue_type(9, p).
residue_type(10, h).

% Coordinate bounds (self-avoiding walk of 10 steps fits easily)
coord_domain(-9..9).

% --- Generation: each residue gets exactly one coordinate ---
1 { coord(R, X, Y) : coord_domain(X), coord_domain(Y) } 1 :- residue(R).

% --- Constraints ---

% 1. Self-avoiding walk: no two residues share the same lattice point
:- residue(R1), residue(R2), R1 < R2,
   coord(R1, X, Y), coord(R2, X, Y).

% 2. Connectivity: consecutive residues must be adjacent (Manhattan distance = 1)
adjacent(X1, Y1, X2, Y2) :-
    coord_domain(X1), coord_domain(Y1),
    coord_domain(X2), coord_domain(Y2),
    |X1 - X2| + |Y1 - Y2| = 1.

:- residue(R), R < 10,
   coord(R, X1, Y1), coord(R + 1, X2, Y2),
   not adjacent(X1, Y1, X2, Y2).

% --- Energy Calculation ---

% A non-sequential H-H contact exists when two H residues (|i-j| > 1)
% occupy adjacent lattice points. Each such contact contributes -1.
contact(R1, R2) :-
    residue(R1), residue(R2), R1 < R2,
    |R1 - R2| > 1,
    residue_type(R1, h), residue_type(R2, h),
    coord(R1, X1, Y1), coord(R2, X2, Y2),
    adjacent(X1, Y1, X2, Y2).

total_energy(E) :- E = #sum { -1, R1, R2 : contact(R1, R2) }.

% --- Optimization: minimize total energy ---
#minimize { -1, R1, R2 : contact(R1, R2) }.

% --- Output ---
#show coord/3.
#show total_energy/1.
#show contact/2.