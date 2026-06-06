% Employees
employee(myers; ortega; paine; schmidt; thomson; wong; yoder; zayre).

% Team selection: each employee is either selected or not
{ selected(E) } :- employee(E).

% At least 4 employees on the team
:- #count { E : selected(E) } < 4.

% Condition 1: If Myers is on the team, neither Ortega nor Paine can be.
:- selected(myers), selected(ortega).
:- selected(myers), selected(paine).

% Condition 2: If Schmidt is on the team, both Paine and Thomson must also be.
:- selected(schmidt), not selected(paine).
:- selected(schmidt), not selected(thomson).

% Condition 3: If Wong is on the team, both Myers and Yoder must also be.
:- selected(wong), not selected(myers).
:- selected(wong), not selected(yoder).

% Test each pair by forcing both to be selected
% We'll test each one individually by adding a constraint

% Let's test pair (A): Myers and Thomson
% Force both selected
:- not selected(myers).
:- not selected(thomson).

#show selected/1.