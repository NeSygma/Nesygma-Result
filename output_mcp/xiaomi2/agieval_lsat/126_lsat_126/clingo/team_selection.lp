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

% Answer choice conditions (what COULD be true)
% A: Neither Myers nor Ortega is on the team
cond_a :- not on(myers), not on(ortega).
% B: Neither Myers nor Thomson is on the team
cond_b :- not on(myers), not on(thomson).
% C: Neither Myers nor Zayre is on the team
cond_c :- not on(myers), not on(zayre).
% D: Neither Ortega nor Thomson is on the team
cond_d :- not on(ortega), not on(thomson).
% E: Neither Ortega nor Yoder is on the team
cond_e :- not on(ortega), not on(yoder).

% A condition "could be true" if there exists a valid model where it holds
% We need to find which options are possible
% Use a selector to pick one option to verify per model
{select(a; b; c; d; e)} 1.

% If we select an option, its condition must hold in this model
:- select(a), not cond_a.
:- select(b), not cond_b.
:- select(c), not cond_c.
:- select(d), not cond_d.
:- select(e), not cond_e.

% Map selected option to output
option(X) :- select(X).

#show option/1.
#show on/1.