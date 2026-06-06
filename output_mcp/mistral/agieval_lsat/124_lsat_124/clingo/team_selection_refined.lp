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

% Check if a pair can be selected together in at least one valid model
% If a pair cannot be selected together in any valid model, it is impossible
impossible_pair(E1, E2) :-
    pair(E1, E2),
    not can_be_together(E1, E2).

can_be_together(E1, E2) :-
    selected(E1),
    selected(E2),
    pair(E1, E2).

% Ensure that if a pair is impossible, no valid selection includes both
:- impossible_pair(E1, E2), selected(E1), selected(E2).

% Map the correct answer to option/1
option(a) :- impossible_pair(myers, thomson).
option(b) :- impossible_pair(ortega, yoder).
option(c) :- impossible_pair(paine, zayre).
option(d) :- impossible_pair(schmidt, wong).
option(e) :- impossible_pair(wong, yoder).

#show option/1.