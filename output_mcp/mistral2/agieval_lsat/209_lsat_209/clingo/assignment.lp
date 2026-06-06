% Define the students and teams
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
assigned_to(lateefah, green).

% Ensure one team has 2 members and the other has 3
num_green(S) :- S = #count { St : assigned_to(St, green) }.
num_red(S) :- S = #count { St : assigned_to(St, red) }.
:- num_green(2), num_red(2).
:- num_green(3), num_red(3).
:- num_green(N), num_red(N).

% Juana and Olga are on different teams
:- assigned_to(juana, T), assigned_to(olga, T), team(T).

% Designate exactly one facilitator per team
1 { facilitator(S, T) : student(S) } 1 :- team(T).

% Olga is a facilitator
facilitator(olga, _).

% Kelly is not a facilitator
:- facilitator(kelly, _).

% Ensure facilitator is on the team they are assigned to
:- facilitator(S, T), not assigned_to(S, T).

% Define the conditions for each option
% (A) Juana is assigned to the red team
option(a) :- assigned_to(juana, red).

% (B) Lateefah is a facilitator
option(b) :- facilitator(lateefah, _).

% (C) Olga is assigned to the green team
option(c) :- assigned_to(olga, green).

% (D) Juana and Mei are not both facilitators
not_both_facilitators :- facilitator(juana, _), facilitator(mei, _).
option(d) :- not not_both_facilitators.

% (E) Neither Juana nor Kelly is a facilitator
option(e) :- not facilitator(juana, _), not facilitator(kelly, _).

#show option/1.