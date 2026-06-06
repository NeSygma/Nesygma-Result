% Protein Folding: HP model on 2D lattice
% Sequence: HPHPHHPHPH (10 residues)
% Use relative moves (directions) between consecutive residues.

% --- Domain ---
residue(1..10).
step(1..9).  % steps between consecutive residues

% Residue types
residue_type(1, h). residue_type(2, p). residue_type(3, h).
residue_type(4, p). residue_type(5, h). residue_type(6, h).
residue_type(7, p). residue_type(8, h). residue_type(9, p).
residue_type(10, h).

% Possible directions: right, up, left, down
direction(r; u; l; d).

% Coordinate bounds
coord_domain(-9..9).

% --- Generation: choose a direction for each step ---
{ move(S, D) : direction(D) } 1 :- step(S).

% --- Coordinate computation ---
% Residue 1 fixed at (0,0)
coord(1, 0, 0).

% Compute coordinates for residues 2..10 based on moves
coord(R+1, X2, Y2) :-
    residue(R), R < 10,
    coord(R, X, Y),
    move(R, D),
    X2 = X + (D = r) - (D = l),
    Y2 = Y + (D = u) - (D = d),
    coord_domain(X2), coord_domain(Y2).

% --- Constraints ---

% 1. Self-avoiding walk: no two residues share the same lattice point
:- residue(R1), residue(R2), R1 < R2,
   coord(R1, X, Y), coord(R2, X, Y).

% 2. Connectivity is enforced by construction (moves define adjacent placement)

% --- Energy Calculation ---

% A non-sequential H-H contact exists when two H residues (|i-j| > 1)
% occupy adjacent lattice points.
adjacent_coord(X1, Y1, X2, Y2) :-
    coord_domain(X1), coord_domain(Y1),
    coord_domain(X2), coord_domain(Y2),
    |X1 - X2| + |Y1 - Y2| = 1.

contact(R1, R2) :-
    residue(R1), residue(R2), R1 < R2,
    |R1 - R2| > 1,
    residue_type(R1, h), residue_type(R2, h),
    coord(R1, X1, Y1), coord(R2, X2, Y2),
    adjacent_coord(X1, Y1, X2, Y2).

total_energy(E) :- E = #sum { -1, R1, R2 : contact(R1, R2) }.

% --- Optimization: minimize total energy ---
#minimize { -1, R1, R2 : contact(R1, R2) }.

% --- Output ---
#show coord/3.
#show total_energy/1.
#show contact/2.