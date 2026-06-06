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
team_size(N) :- N = #count { E : on_team(E) }, N >= 4.

% Choice rule: select employees for the team
{ on_team(E) : employee(E) }.

% Selection constraints
% 1. If Myers is on the team, neither Ortega nor Paine can be.
:- on_team(myers), on_team(ortega).
:- on_team(myers), on_team(paine).

% 2. If Schmidt is on the team, both Paine and Thomson must also be.
:- on_team(schmidt), not on_team(paine).
:- on_team(schmidt), not on_team(thomson).

% 3. If Wong is on the team, both Myers and Yoder must also be.
:- on_team(wong), not on_team(myers).
:- on_team(wong), not on_team(yoder).

% Define the team selections for each option
% Option A: Myers, Paine, Schmidt, and Thomson
option(a) :- on_team(myers), on_team(paine), on_team(schmidt), on_team(thomson),
             not on_team(ortega), not on_team(wong), not on_team(yoder), not on_team(zayre),
             team_size(4).

% Option B: Ortega, Paine, Thomson, and Zayre
option(b) :- on_team(ortega), on_team(paine), on_team(thomson), on_team(zayre),
             not on_team(myers), not on_team(schmidt), not on_team(wong), not on_team(yoder),
             team_size(4).

% Option C: Paine, Schmidt, Yoder, and Zayre
option(c) :- on_team(paine), on_team(schmidt), on_team(yoder), on_team(zayre),
             not on_team(myers), not on_team(ortega), not on_team(thomson), not on_team(wong),
             team_size(4).

% Option D: Schmidt, Thomson, Yoder, and Zayre
option(d) :- on_team(schmidt), on_team(thomson), on_team(yoder), on_team(zayre),
             not on_team(myers), not on_team(ortega), not on_team(paine), not on_team(wong),
             team_size(4).

% Option E: Thomson, Wong, Yoder, and Zayre
option(e) :- on_team(thomson), on_team(wong), on_team(yoder), on_team(zayre),
             not on_team(myers), not on_team(ortega), not on_team(paine), not on_team(schmidt),
             team_size(4).

% Show the selected option
#show option/1.