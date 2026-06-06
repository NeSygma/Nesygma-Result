% Define the employees
domain(myers).
domain(ortega).
domain(paine).
domain(schmidt).
domain(thomson).
domain(wong).
domain(yoder).
domain(zayre).

% Choice rule: select employees for the team
{ on_team(E) : domain(E) }.

% The team must have at least 4 employees
team_size(N) :- N = #count{E : on_team(E)}.
:- team_size(N), N < 4.

% Constraints
% If Myers is on the team, neither Ortega nor Paine can be
:- on_team(myers), on_team(ortega).
:- on_team(myers), on_team(paine).

% If Schmidt is on the team, both Paine and Thomson must also be
:- on_team(schmidt), not on_team(paine).
:- on_team(schmidt), not on_team(thomson).

% If Wong is on the team, both Myers and Yoder must also be
:- on_team(wong), not on_team(myers).
:- on_team(wong), not on_team(yoder).

% Condition: Paine is NOT on the team
:- on_team(paine).

% Define the options
% (A) Neither Myers nor Ortega is on the team
option(a) :- not on_team(myers), not on_team(ortega).

% (B) Neither Myers nor Thomson is on the team
option(b) :- not on_team(myers), not on_team(thomson).

% (C) Neither Myers nor Zayre is on the team
option(c) :- not on_team(myers), not on_team(zayre).

% (D) Neither Ortega nor Thomson is on the team
option(d) :- not on_team(ortega), not on_team(thomson).

% (E) Neither Ortega nor Yoder is on the team
option(e) :- not on_team(ortega), not on_team(yoder).

#show option/1.