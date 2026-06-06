% Employees
employee(myers). employee(ortega). employee(paine). employee(schmidt).
employee(thomson). employee(wong). employee(yoder). employee(zayre).

% Choose team members (at least 4)
{on(X)} :- employee(X).
:- #count{X : on(X)} < 4.

% Constraint 1: If Myers is on team, neither Ortega nor Paine can be
:- on(myers), on(ortega).
:- on(myers), on(paine).

% Constraint 2: If Schmidt is on team, both Paine and Thomson must be
:- on(schmidt), not on(paine).
:- on(schmidt), not on(thomson).

% Constraint 3: If Wong is on team, both Myers and Yoder must be
:- on(wong), not on(myers).
:- on(wong), not on(yoder).

% Given: Paine is NOT on the team
:- on(paine).

% Check option A: Neither Myers nor Ortega is on the team
% Force this condition and see if satisfiable
check_a :- not on(myers), not on(ortega).
:- not check_a.

#show on/1.