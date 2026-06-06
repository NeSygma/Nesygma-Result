% Students
student(juana).
student(kelly).
student(lateefah).
student(mei).
student(olga).

% Team assignment: each student assigned to exactly one team
{ team(green, X) ; team(red, X) } 1 :- student(X).

% Team size constraints
#count{ X : team(green, X), student(X) } = 3.
#count{ X : team(red,   X), student(X) } = 2.

% Exactly one facilitator per team
#count{ X : facilitator(X), team(green, X), student(X) } = 1.
#count{ X : facilitator(X), team(red,   X), student(X) } = 1.

% Facilitator facts and constraints
facilitator(olga).               % Olga is a facilitator
:- facilitator(kelly).           % Kelly is not a facilitator

% Juana and Olga on different teams
:- team(T, juana), team(T, olga).

% Premise: Mei is assigned to the green team (for the question)
team(green, mei).

% Derive options based on answer choices
option(a) :- team(green, juana).
option(b) :- team(red, kelly).
option(c) :- team(green, olga).
option(d) :- facilitator(lateefah).
option(e) :- facilitator(mei).

% Show derived options
#show option/1.