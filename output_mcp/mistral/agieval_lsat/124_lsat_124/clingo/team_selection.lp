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

% Check if a pair can be selected together
can_be_together(E1, E2) :- selected(E1), selected(E2), pair(E1, E2).

% Determine which pair cannot be together
impossible_pair(myers, thomson) :- pair(myers, thomson), not can_be_together(myers, thomson).
impossible_pair(ortega, yoder) :- pair(ortega, yoder), not can_be_together(ortega, yoder).
impossible_pair(paine, zayre) :- pair(paine, zayre), not can_be_together(paine, zayre).
impossible_pair(schmidt, wong) :- pair(schmidt, wong), not can_be_together(schmidt, wong).
impossible_pair(wong, yoder) :- pair(wong, yoder), not can_be_together(wong, yoder).

% Map the correct answer to option/1
option(a) :- impossible_pair(myers, thomson).
option(b) :- impossible_pair(ortega, yoder).
option(c) :- impossible_pair(paine, zayre).
option(d) :- impossible_pair(schmidt, wong).
option(e) :- impossible_pair(wong, yoder).

#show option/1.