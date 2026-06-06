% Define the sequence length
residue(1..10).

% Residue types (HPHPHHPHPH)
type(1, "H"). type(2, "P"). type(3, "H"). type(4, "P"). type(5, "H").
type(6, "H"). type(7, "P"). type(8, "H"). type(9, "P"). type(10, "H").

% Helper: H residues
h(Pos) :- type(Pos, "H").

% Define coordinate domain - we need to bound the lattice
% For a 10-residue protein, a 6x6 grid should be sufficient
x(0..5). y(0..5).

% Precompute all adjacent coordinate pairs
adj(X1,Y1,X2,Y2) :-
    x(X1), y(Y1), x(X2), y(Y2),
    (X1 - X2) * (X1 - X2) + (Y1 - Y2) * (Y1 - Y2) = 1.

% Choice rule: assign coordinates to each residue
{ coord(Pos, X, Y) : x(X), y(Y) } = 1 :- residue(Pos).

% Self-avoiding walk: all coordinates must be unique
:- coord(Pos1, X, Y), coord(Pos2, X, Y), Pos1 != Pos2.

% Connectivity: consecutive residues must be adjacent
:- residue(Pos), residue(Pos+1),
   coord(Pos, X1, Y1), coord(Pos+1, X2, Y2),
   not adj(X1,Y1,X2,Y2).

% Non-sequential H-H contacts: |i-j| > 1 and adjacent on lattice
contact(Pos1, Pos2) :-
    h(Pos1), h(Pos2),
    Pos1 < Pos2,
    Pos2 - Pos1 > 1,  % |i-j| > 1
    coord(Pos1, X1, Y1),
    coord(Pos2, X2, Y2),
    adj(X1,Y1,X2,Y2).

% Count the number of contacts
num_contacts(C) :-
    C = #count{ Pos1, Pos2 : contact(Pos1, Pos2) }.

% Calculate total energy (each contact contributes -1)
energy(E) :-
    num_contacts(C),
    E = 0 - C.

% Minimize energy (most negative = minimum)
#minimize{ E : energy(E) }.

% Show the coordinates for the solution
#show coord/3.
#show energy/1.