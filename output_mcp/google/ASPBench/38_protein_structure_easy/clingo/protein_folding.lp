% Protein sequence: H P H P P H H H
% Indices:        1 2 3 4 5 6 7 8
type(1, h). type(2, p). type(3, h). type(4, p).
type(5, p). type(6, h). type(7, h). type(8, h).

% Grid size
size(0..7).

% Each residue must be placed on a unique lattice point
1 { at(R, X, Y) : size(X), size(Y) } 1 :- R = 1..8.
:- at(R1, X, Y), at(R2, X, Y), R1 != R2.

% Consecutive residues must be adjacent (Manhattan distance = 1)
dist1(X1, Y1, X2, Y2) :- size(X1), size(Y1), size(X2), size(Y2), |X1-X2| + |Y1-Y2| == 1.
:- R = 1..7, at(R, X1, Y1), at(R+1, X2, Y2), not dist1(X1, Y1, X2, Y2).

% H-H contact between non-sequential residues
h_contact(R1, R2) :- 
    type(R1, h), type(R2, h), 
    R1 + 1 < R2, 
    at(R1, X1, Y1), at(R2, X2, Y2), 
    dist1(X1, Y1, X2, Y2).

% Energy calculation
num_contacts(N) :- N = #count { R1, R2 : h_contact(R1, R2) }.
energy(E) :- num_contacts(N), E = -N.

% Objective: Minimize energy (maximize contacts)
#minimize { E : energy(E) }.

% Output
#show at/3.
#show energy/1.