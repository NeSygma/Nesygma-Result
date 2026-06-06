% Define employees
employee(m;o;p;s;t;w;y;z).

% Team selection: each employee may be on the team
{ on_team(X) } :- employee(X).

% At least 4 members
:- #count{X : on_team(X)} < 4.

% Condition 1: If Myers is on team, neither Ortega nor Paine can be.
:- on_team(m), on_team(o).
:- on_team(m), on_team(p).

% Condition 2: If Schmidt is on team, both Paine and Thomson must also be.
:- on_team(s), not on_team(p).
:- on_team(s), not on_team(t).

% Condition 3: If Wong is on team, both Myers and Yoder must also be.
:- on_team(w), not on_team(m).
:- on_team(w), not on_team(y).

% Given: Paine is not on the team
:- on_team(p).

% --- Evaluate each option ---
% Choose exactly one option scenario
1 { scenario(1..5) } 1.

% Option A: Neither Myers nor Ortega is on the team.
:- scenario(1), on_team(m).
:- scenario(1), on_team(o).

% Option B: Neither Myers nor Thomson is on the team.
:- scenario(2), on_team(m).
:- scenario(2), on_team(t).

% Option C: Neither Myers nor Zayre is on the team.
:- scenario(3), on_team(m).
:- scenario(3), on_team(z).

% Option D: Neither Ortega nor Thomson is on the team.
:- scenario(4), on_team(o).
:- scenario(4), on_team(t).

% Option E: Neither Ortega nor Yoder is on the team.
:- scenario(5), on_team(o).
:- scenario(5), on_team(y).

% Map scenario to answer
option(a) :- scenario(1).
option(b) :- scenario(2).
option(c) :- scenario(3).
option(d) :- scenario(4).
option(e) :- scenario(5).

#show option/1.