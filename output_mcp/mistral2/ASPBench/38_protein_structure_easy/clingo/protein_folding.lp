% --- Domain ---
residue(1..8).
x(0..4).
y(0..4).
coordinate(X, Y) :- x(X), y(Y).

% --- Sequence ---
sequence(1, "H").
sequence(2, "P").
sequence(3, "P").
sequence(4, "H").
sequence(5, "P").
sequence(6, "P").
sequence(7, "H").
sequence(8, "H").

% --- Adjacency ---
adjacent(X1, Y1, X2, Y2) :-
    coordinate(X1, Y1), coordinate(X2, Y2),
    (X1 = X2, (Y1 = Y2 + 1 ; Y1 = Y2 - 1)) ;
    (Y1 = Y2, (X1 = X2 + 1 ; X1 = X2 - 1)).

% --- Placement ---
1 { placed(R, X, Y) : coordinate(X, Y) } 1 :- residue(R).

% --- Consecutive residues must be adjacent ---
:- residue(R), residue(R+1),
   not adjacent(X1, Y1, X2, Y2),
   placed(R, X1, Y1), placed(R+1, X2, Y2).

% --- Self-avoiding walk ---
:- placed(R1, X, Y), placed(R2, X, Y), R1 != R2.

% --- Contacts (non-sequential neighbors) ---
contact(R1, R2) :-
    placed(R1, X1, Y1), placed(R2, X2, Y2),
    adjacent(X1, Y1, X2, Y2),
    |R1 - R2| > 1.

% --- H-H contacts ---
hh_contact(R1, R2) :-
    contact(R1, R2),
    sequence(R1, "H"),
    sequence(R2, "H").

% --- Energy calculation ---
energy(E) :- E = #sum { -1, R1, R2 : hh_contact(R1, R2) }.

% --- Minimize energy ---
#minimize { E : energy(E) }.

% --- Show coordinates ---
#show placed/3.