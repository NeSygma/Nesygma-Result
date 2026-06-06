% Define the employees
employee(myers).
employee(ortega).
employee(paine).
employee(schmidt).
employee(thomson).
employee(wong).
employee(yoder).
employee(zayre).

% The team must have at least 4 employees
1 { selected(E) : employee(E) } 4.

% Constraint 1: If Myers is on the team, neither Ortega nor Paine can be.
:- selected(myers), selected(ortega).
:- selected(myers), selected(paine).

% Constraint 2: If Schmidt is on the team, both Paine and Thomson must also be.
:- selected(schmidt), not selected(paine).
:- selected(schmidt), not selected(thomson).

% Constraint 3: If Wong is on the team, both Myers and Yoder must also be.
:- selected(wong), not selected(myers).
:- selected(wong), not selected(yoder).

% Define the pairs for the answer choices
pair(myers_thomson).
pair(ortega_yoder).
pair(paine_zayre).
pair(schmidt_wong).
pair(wong_yoder).

% Helper predicates to check if a pair is selected together
selected_pair(myers_thomson) :- selected(myers), selected(thomson).
selected_pair(ortega_yoder) :- selected(ortega), selected(yoder).
selected_pair(paine_zayre) :- selected(paine), selected(zayre).
selected_pair(schmidt_wong) :- selected(schmidt), selected(wong).
selected_pair(wong_yoder) :- selected(wong), selected(yoder).

% The pair that cannot be selected together is the one that is never valid
% We need to find which pair is impossible to have together in any valid team

% Map the correct answer to option/1
option(a) :- not selected_pair(myers_thomson).
option(b) :- not selected_pair(ortega_yoder).
option(c) :- not selected_pair(paine_zayre).
option(d) :- not selected_pair(schmidt_wong).
option(e) :- not selected_pair(wong_yoder).

#show option/1.