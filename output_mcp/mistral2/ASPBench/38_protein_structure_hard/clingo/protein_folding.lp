% --- Facts: Protein sequence ---
position(1..10).
residue(1, h). residue(2, p). residue(3, h). residue(4, p). residue(5, h).
residue(6, h). residue(7, p). residue(8, h). residue(9, p). residue(10, h).

% --- Domain for coordinates ---
x_coordinate(-10..10).
y_coordinate(-10..10).

% --- Choice Rule: Assign coordinates to residues ---
{ coordinate(Pos, X, Y) : x_coordinate(X), y_coordinate(Y) } 1 :- position(Pos).

% --- Adjacency helper ---
% Define all possible adjacent coordinate pairs
adjacent(X1, Y1, X2, Y2) :-
    x_coordinate(X1), y_coordinate(Y1), x_coordinate(X2), y_coordinate(Y2),
    (X2 = X1 + 1, Y2 = Y1) ;
    (X2 = X1 - 1, Y2 = Y1) ;
    (X2 = X1, Y2 = Y1 + 1) ;
    (X2 = X1, Y2 = Y1 - 1).

% --- Connectivity: Consecutive residues must be adjacent ---
:- position(Pos), position(NextPos), NextPos = Pos + 1,
   coordinate(Pos, X1, Y1), coordinate(NextPos, X2, Y2),
   not adjacent(X1, Y1, X2, Y2).

% --- Self-avoiding walk: All coordinates must be unique ---
:- coordinate(Pos1, X, Y), coordinate(Pos2, X, Y), Pos1 != Pos2.

% --- Non-sequential H-H contacts ---
% Define a contact between Pos1 and Pos2 if:
% 1. |Pos1 - Pos2| > 1
% 2. Both residues are H
% 3. Their coordinates are adjacent
contact(Pos1, Pos2) :-
    position(Pos1), position(Pos2),
    Pos1 < Pos2, % Avoid duplicate pairs
    (Pos2 - Pos1) > 1,
    residue(Pos1, h), residue(Pos2, h),
    coordinate(Pos1, X1, Y1), coordinate(Pos2, X2, Y2),
    adjacent(X1, Y1, X2, Y2).

% --- Energy calculation ---
% Each contact contributes -1 to energy.
energy(E) :- E = #count{ Pos1, Pos2 : contact(Pos1, Pos2) }.

% --- Objective: Minimize energy ---
#minimize{ E : energy(E) }.

% --- Show the solution ---
#show coordinate/3.
#show energy/1.