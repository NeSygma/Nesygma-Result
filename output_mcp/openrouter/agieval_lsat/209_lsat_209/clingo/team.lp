% Students and teams
student(juana). student(kelly). student(lateefah). student(mei). student(olga).
team(green). team(red).

% Each student assigned to exactly one team
1 { assigned(S,T) : team(T) } 1 :- student(S).

% Team size: green must have 2 or 3 members (the other will be 3 or 2)
:- #count{ S : assigned(S,green) } = G, G != 2, G != 3.

% Facilitator constraints
% Each team has exactly one facilitator
1 { facilitator(S) : assigned(S,green) } 1 :- team(green).
1 { facilitator(S) : assigned(S,red) } 1 :- team(red).

% Facilitator must be assigned to a team
:- facilitator(S), not assigned(S,_).

% Problem specific constraints
% Juana different team than Olga
:- assigned(juana,T), assigned(olga,T).
% Lateefah is green
assigned(lateefah,green).
% Kelly not facilitator
:- facilitator(kelly).
% Olga is a facilitator
facilitator(olga).

% Helper predicate for both Juana and Mei being facilitators
both_facilitators :- facilitator(juana), facilitator(mei).

% Options mapping
option(a) :- assigned(juana,red).
option(b) :- facilitator(lateefah).
option(c) :- assigned(olga,green).
option(d) :- not both_facilitators.
option(e) :- not facilitator(juana), not facilitator(kelly).

% Exactly one option must be selected
1 { option(a); option(b); option(c); option(d); option(e) } 1.

#show option/1.