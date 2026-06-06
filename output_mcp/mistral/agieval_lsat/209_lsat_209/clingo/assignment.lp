% Domain
student(juana; kelly; lateefah; mei; olga).
team(green; red).

% Facts from problem
assigned(lateefah, green).  % Lateefah is assigned to the green team
:- assigned(juana, T), assigned(olga, T).  % Juana and Olga on different teams
:- facilitator(_, kelly).  % Kelly is not a facilitator

% Each student assigned to exactly one team
1 { assigned(S, T) : team(T) } 1 :- student(S).

% Team sizes: one team has 2 members, the other has 3
team_size(T, 2) :- team(T), #count { S : assigned(S, T) } = 2.
team_size(T, 3) :- team(T), #count { S : assigned(S, T) } = 3.
:- team(T1), team(T2), T1 != T2, team_size(T1, 2), team_size(T2, 2).
:- team(T1), team(T2), T1 != T2, team_size(T1, 3), team_size(T2, 3).

% Exactly one facilitator per team, and facilitator must be on the team
1 { facilitator(T, S) : student(S) } 1 :- team(T).
:- facilitator(T, S), not assigned(S, T).

% Olga is a facilitator (must be facilitator of her team)
:- assigned(olga, T), not facilitator(T, olga).

% Helper predicate for Juana and Mei both being facilitators
both_facilitators :- facilitator(_, juana), facilitator(_, mei).

% Map the correct answer to option/1
% Option A: Juana is assigned to the red team
option(a) :- assigned(juana, red).

% Option B: Lateefah is a facilitator
option(b) :- facilitator(_, lateefah).

% Option C: Olga is assigned to the green team
option(c) :- assigned(olga, green).

% Option D: Juana and Mei are not both facilitators
option(d) :- not both_facilitators.

% Option E: Neither Juana nor Kelly is a facilitator
option(e) :- not facilitator(_, juana), not facilitator(_, kelly).

#show option/1.