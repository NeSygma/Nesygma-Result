% Base facts: students and teams
student(juana).
student(kelly).
student(lateefah).
student(mei).
student(olga).
team(green).
team(red).

% Assign each student to exactly one team
1 { assigned_to(S, T) : team(T) } 1 :- student(S).

% Lateefah is assigned to the green team
:- not assigned_to(lateefah, green).

% Juana is assigned to a different team than Olga
:- assigned_to(juana, T), assigned_to(olga, T), team(T).

% Team sizes: one team has 2 members, the other has 3
:- { assigned_to(S, green) : student(S) } != 2, { assigned_to(S, green) : student(S) } != 3.
:- { assigned_to(S, red) : student(S) } != 2, { assigned_to(S, red) : student(S) } != 3.
:- { assigned_to(S, green) : student(S) } = 2, { assigned_to(S, red) : student(S) } = 2.
:- { assigned_to(S, green) : student(S) } = 3, { assigned_to(S, red) : student(S) } = 3.

% Facilitator assignment: exactly one facilitator per team
1 { facilitator(S, T) : student(S) } 1 :- team(T).

% Kelly is not a facilitator
:- facilitator(kelly, _).

% Olga is a facilitator
:- not facilitator(olga, _).

% Facilitator must be a member of the team they facilitate
:- facilitator(S, T), not assigned_to(S, T).

% If Mei is assigned to the green team, derive the answer
mei_green :- assigned_to(mei, green).

% Map the correct answer to option/1 based on the condition
% (A) Juana is assigned to the green team.
option(a) :- mei_green, assigned_to(juana, green).

% (B) Kelly is assigned to the red team.
option(b) :- mei_green, assigned_to(kelly, red).

% (C) Olga is assigned to the green team.
option(c) :- mei_green, assigned_to(olga, green).

% (D) Lateefah is a facilitator.
option(d) :- mei_green, facilitator(lateefah, _).

% (E) Mei is a facilitator.
option(e) :- mei_green, facilitator(mei, _).

#show option/1.