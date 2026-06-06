% Base facts: employees
employee(myers).
employee(ortega).
employee(paine).
employee(schmidt).
employee(thomson).
employee(wong).
employee(yoder).
employee(zayre).

% Team size constraint: at least 4 employees
team_size(N) :- N = #count { E : employee(E), selected(E) }, N >= 4.

% Selection choice rule
{ selected(E) : employee(E) }.

% Constraints

% If Myers is on the team, neither Ortega nor Paine can be
:- selected(myers), selected(ortega).
:- selected(myers), selected(paine).

% If Schmidt is on the team, both Paine and Thomson must also be
:- selected(schmidt), not selected(paine).
:- selected(schmidt), not selected(thomson).

% If Wong is on the team, both Myers and Yoder must also be
:- selected(wong), not selected(myers).
:- selected(wong), not selected(yoder).

% Given condition: Paine is not on the team
:- selected(paine).

% Ensure team size constraint is satisfied
:- not team_size(_).

% Map the correct answer to option/1 (MANDATORY)
% We need to check which of the options (A-E) could be true under the given constraints

% Define helper predicates for each option

% Option A: Neither Myers nor Ortega is on the team
option(a) :- not selected(myers), not selected(ortega).

% Option B: Neither Myers nor Thomson is on the team
option(b) :- not selected(myers), not selected(thomson).

% Option C: Neither Myers nor Zayre is on the team
option(c) :- not selected(myers), not selected(zayre).

% Option D: Neither Ortega nor Thomson is on the team
option(d) :- not selected(ortega), not selected(thomson).

% Option E: Neither Ortega nor Yoder is on the team
option(e) :- not selected(ortega), not selected(yoder).

#show option/1.