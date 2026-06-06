% Base constraints + original constraint 4 -> get all models

photographer(f; g; h; k; l; m).
ceremony(silva; thorne).

0 { assign(P, C) : ceremony(C) } 1 :- photographer(P).

% At least 2 per ceremony
:- #count { P : assign(P, silva) } < 2.
:- #count { P : assign(P, thorne) } < 2.

% Constraint 1: Frost and Heideck together at same ceremony, both assigned
:- assign(f, C1), assign(h, C2), C1 != C2.
assigned(P) :- assign(P, _).
:- not assigned(f).
:- not assigned(h).

% Constraint 2: Lai and Mays cannot be at same ceremony if both assigned
:- assign(l, C), assign(m, C).

% Constraint 3: Gonzalez at Silva -> Lai at Thorne
:- assign(g, silva), not assign(l, thorne).

% Original constraint 4:
% If Knutson is not assigned to Thorne, then both Heideck and Mays must be assigned to Thorne
:- not assign(k, thorne), not assign(h, thorne).
:- not assign(k, thorne), not assign(m, thorne).

#show assign/2.