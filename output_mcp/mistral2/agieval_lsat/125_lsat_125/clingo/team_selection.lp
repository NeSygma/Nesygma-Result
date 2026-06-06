% Domain of employees
employee(myers).
employee(ortega).
employee(paine).
employee(schmidt).
employee(thomson).
employee(wong).
employee(yoder).
employee(zayre).

% Team size constraint (at least 4)
size(4..8).

% Assume Yoder is not on the team
not_on_team(yoder).

% Choice rule for team members
{ on_team(E) : employee(E) }.

% Team size constraint
:- size(S), #count{ E : on_team(E) } < S.

% Constraint 1: If Myers is on the team, neither Ortega nor Paine can be
:- on_team(myers), on_team(ortega).
:- on_team(myers), on_team(paine).

% Constraint 2: If Schmidt is on the team, both Paine and Thomson must be
:- on_team(schmidt), not on_team(paine).
:- on_team(schmidt), not on_team(thomson).

% Constraint 3: If Wong is on the team, both Myers and Yoder must be
:- on_team(wong), not on_team(myers).
:- on_team(wong), not on_team(yoder).

% Yoder is not on the team (already enforced by not_on_team(yoder))
:- on_team(yoder).

% Check if each option can be on the team
% (A) Zayre: Possible if no constraints are violated
possible_zayre :- on_team(zayre).

% (B) Thomson: Possible if Schmidt is not on the team or if Schmidt is on the team (Paine must also be on the team)
possible_thomson :- on_team(thomson).

% (C) Paine: Possible if Schmidt is not on the team or if Schmidt is on the team (Paine and Thomson must be on the team)
possible_paine :- on_team(paine).

% (D) Ortega: Possible if Myers is not on the team
possible_ortega :- on_team(ortega).

% (E) Myers: Possible if Wong is not on the team (since Yoder is not on the team, Wong cannot be on the team)
possible_myers :- on_team(myers).

% The correct answer is the option that CANNOT be on the team
% We need to check which of the above is impossible

% If Zayre cannot be on the team, then option(a) is correct
option(a) :- not possible_zayre.

% If Thomson cannot be on the team, then option(b) is correct
option(b) :- not possible_thomson.

% If Paine cannot be on the team, then option(c) is correct
option(c) :- not possible_paine.

% If Ortega cannot be on the team, then option(d) is correct
option(d) :- not possible_ortega.

% If Myers cannot be on the team, then option(e) is correct
option(e) :- not possible_myers.

#show option/1.