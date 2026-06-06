% Employees
employee(myers). employee(ortega). employee(paine). employee(schmidt). employee(thomson). employee(wong). employee(yoder). employee(zayre).

% Choose team members (any subset)
{team(P) : employee(P)}.

% At least four members
:- #count{P : team(P)} < 4.

% Constraints
% If Myers is on the team, neither Ortega nor Paine can be.
:- team(myers), team(ortega).
:- team(myers), team(paine).
% If Schmidt is on the team, both Paine and Thomson must also be.
:- team(schmidt), not team(paine).
:- team(schmidt), not team(thomson).
% If Wong is on the team, both Myers and Yoder must also be.
:- team(wong), not team(myers).
:- team(wong), not team(yoder).

% Define absent predicates for each pair (true when both are absent)
absentA :- not team(ortega), not team(schmidt).   % A: Ortega and Schmidt
absentB :- not team(ortega), not team(wong).      % B: Ortega and Wong
absentC :- not team(paine), not team(schmidt).    % C: Paine and Schmidt
absentD :- not team(thomson), not team(yoder).    % D: Thomson and Yoder
absentE :- not team(yoder), not team(zayre).      % E: Yoder and Zayre

% Map options: an option is possible only if its pair cannot be both absent
option(a) :- not absentA.
option(b) :- not absentB.
option(c) :- not absentC.
option(d) :- not absentD.
option(e) :- not absentE.

% Exactly one option must be true
1 { option(a); option(b); option(c); option(d); option(e) } 1.

#show option/1.