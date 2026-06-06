% Define the employees
employee(myers).
employee(ortega).
employee(paine).
employee(schmidt).
employee(thomson).
employee(wong).
employee(yoder).
employee(zayre).

% Choice rule for selecting employees
{ selected(E) : employee(E) }.

% Team must have at least 4 employees
:- #count{ E : selected(E) } < 4.

% Constraint 1: If Myers is on the team, neither Ortega nor Paine can be
:- selected(myers), selected(ortega).
:- selected(myers), selected(paine).

% Constraint 2: If Schmidt is on the team, both Paine and Thomson must also be
:- selected(schmidt), not selected(paine).
:- selected(schmidt), not selected(thomson).

% Constraint 3: If Wong is on the team, both Myers and Yoder must also be
:- selected(wong), not selected(myers).
:- selected(wong), not selected(yoder).

% Define pairs for each option
pair(myers, thomson).
pair(ortega, yoder).
pair(paine, zayre).
pair(schmidt, wong).
pair(wong, yoder).

% Check if a pair cannot be selected together in any valid model
% If a pair cannot be selected together, mark the corresponding option as correct
option(a) :- pair(myers, thomson), not possible_pair(myers, thomson).
option(b) :- pair(ortega, yoder), not possible_pair(ortega, yoder).
option(c) :- pair(paine, zayre), not possible_pair(paine, zayre).
option(d) :- pair(schmidt, wong), not possible_pair(schmidt, wong).
option(e) :- pair(wong, yoder), not possible_pair(wong, yoder).

% Helper to check if a pair can be selected together
possible_pair(E1, E2) :-
    selected(E1),
    selected(E2),
    pair(E1, E2).

#show option/1.