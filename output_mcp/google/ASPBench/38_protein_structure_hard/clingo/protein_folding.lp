% --- Domain ---
residue(1..10).
type(1, h). type(2, p). type(3, h). type(4, p). type(5, h).
type(6, h). type(7, p). type(8, h). type(9, p). type(10, h).

% --- Lattice ---
% A 10-residue chain fits easily in a 10x10 grid.
coord(0..10, 0..10).

% --- Choice Rule: Assign each residue to a coordinate ---
{ pos(R, X, Y) : coord(X, Y) } = 1 :- residue(R).

% --- Constraints ---
% 1. Self-avoiding walk: Each residue must occupy a unique lattice point
:- pos(R1, X, Y), pos(R2, X, Y), R1 != R2.

% 2. Connectivity: Consecutive residues must be adjacent (Manhattan distance = 1)
dist(R, D) :- R=1..9, pos(R, X1, Y1), pos(R+1, X2, Y2), D = |X1-X2| + |Y1-Y2|.
:- dist(R, D), D != 1.

% 3. Non-sequential contacts: |i - j| > 1, both H, adjacent
contact(R1, R2) :- residue(R1), residue(R2), R1 < R2 - 1, 
                   type(R1, h), type(R2, h),
                   pos(R1, X1, Y1), pos(R2, X2, Y2),
                   |X1-X2| + |Y1-Y2| == 1.

% 4. Energy calculation
num_contacts(N) :- N = #count { R1, R2 : contact(R1, R2) }.
energy(E) :- num_contacts(N), E = -N.

% --- Objective ---
#minimize { E : energy(E) }.

% --- Output ---
#show pos/3.
#show energy/1.