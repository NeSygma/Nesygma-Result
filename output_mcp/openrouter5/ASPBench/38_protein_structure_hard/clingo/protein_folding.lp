% Protein Folding: HP model on 2D lattice
% Sequence: HPHPHHPHPH (10 residues)

% Define the sequence
residue(1..10).

% Residue types
h(1). p(2). h(3). p(4). h(5). h(6). p(7). h(8). p(9). h(10).

% Define the lattice domain (bound the search space)
% For 10 residues, max coordinate range is roughly -5 to 5
coord(-5..5).

% Each residue gets exactly one (x,y) coordinate
1 { pos(I, X, Y) : coord(X), coord(Y) } 1 :- residue(I).

% Constraint 1: Self-avoiding walk - each lattice point occupied by at most one residue
:- pos(I1, X, Y), pos(I2, X, Y), I1 != I2.

% Constraint 2: Connectivity - consecutive residues must be adjacent (Manhattan distance = 1)
% Define adjacency: Manhattan distance = 1
adj(X1, Y1, X2, Y2) :- coord(X1), coord(Y1), coord(X2), coord(Y2), |X1-X2| = 1, Y1 = Y2.
adj(X1, Y1, X2, Y2) :- coord(X1), coord(Y1), coord(X2), coord(Y2), X1 = X2, |Y1-Y2| = 1.

:- pos(I, X1, Y1), pos(I+1, X2, Y2), not adj(X1, Y1, X2, Y2).

% Energy: Non-sequential H-H contacts
% Two H residues i,j with |i-j| > 1 that are adjacent on the lattice contribute -1 energy
contact(I, J) :- h(I), h(J), I < J, J - I > 1, pos(I, X1, Y1), pos(J, X2, Y2), adj(X1, Y1, X2, Y2).

% Minimize energy (maximize negative contacts)
#minimize { -1, I, J : contact(I, J) }.

% Show results
#show pos/3.
#show contact/2.