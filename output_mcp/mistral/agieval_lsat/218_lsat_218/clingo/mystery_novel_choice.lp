% Base problem setup
chapter(1..7).
clue(r; s; t; u; w; x; z).

% Each clue appears exactly once
1 { assigned(C, Cl) : clue(Cl) } 1 :- chapter(C).
:- clue(Cl), chapter(C1), chapter(C2), C1 != C2, assigned(C1, Cl), assigned(C2, Cl).

% Constraint 2: T must be before W with exactly two chapters separating them
% If T is in chapter C, W must be in chapter C+3
:- assigned(C, t), assigned(C2, w), C2 != C+3.

% Constraint 3: S and Z cannot be adjacent
:- assigned(C, s), assigned(C+1, z).
:- assigned(C, z), assigned(C+1, s).
:- assigned(C, s), assigned(C-1, z).
:- assigned(C, z), assigned(C-1, s).

% Constraint 4: W and X cannot be adjacent
:- assigned(C, w), assigned(C+1, x).
:- assigned(C, x), assigned(C+1, w).
:- assigned(C, w), assigned(C-1, x).
:- assigned(C, x), assigned(C-1, w).

% Constraint 5: U and X must be adjacent
:- assigned(C, u), not assigned(C+1, x), not assigned(C-1, x).
:- assigned(C, x), not assigned(C+1, u), not assigned(C-1, u).

% Original constraint: T cannot be mentioned in chapter 1
:- assigned(1, t).

% --- Substitution options ---

% Helper predicate: W cannot be in chapter 4
w_not_in_4 :- not assigned(4, w).

% Helper predicate: Original constraint (T not in chapter 1)
t_not_in_1 :- not assigned(1, t).

% Option B: W cannot be mentioned in chapter 4
% This is equivalent to the original constraint because of the T-W separation rule
option(b) :- w_not_in_4, t_not_in_1.

% Options A, C, D, E are not equivalent to the original constraint
% They are included here for completeness but will not be derived
option(a) :- not option(b), not option(c), not option(d), not option(e).
option(c) :- not option(a), not option(b), not option(d), not option(e).
option(d) :- not option(a), not option(b), not option(c), not option(e).
option(e) :- not option(a), not option(b), not option(c), not option(d).

#show option/1.