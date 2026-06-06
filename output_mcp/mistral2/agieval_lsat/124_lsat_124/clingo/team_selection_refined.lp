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
pair(myers_thomson, myers, thomson).
pair(ortega_yoder, ortega, yoder).
pair(paine_zayre, paine, zayre).
pair(schmidt_wong, schmidt, wong).
pair(wong_yoder, wong, yoder).

% Check which pair cannot be selected together
% If selecting a pair leads to a contradiction, it cannot be on the team together
impossible_pair(E1, E2) :-
    pair(_, E1, E2),
    selected(E1),
    selected(E2),
    :- selected(E1), selected(E2).

% Map the correct answer to option/1
option(a) :- impossible_pair(myers, thomson).
option(b) :- impossible_pair(ortega, yoder).
option(c) :- impossible_pair(paine, zayre).
option(d) :- impossible_pair(schmidt, wong).
option(e) :- impossible_pair(wong, yoder).

#show option/1.