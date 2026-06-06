% Domain
student(juana). student(kelly). student(lateefah). student(mei). student(olga).
team(green). team(red).

% Each student assigned to exactly one team
1 { assigned(S, T) : team(T) } 1 :- student(S).

% Count team sizes
team_size(green, N) :- N = #count { S : assigned(S, green) }.
team_size(red, N) :- N = #count { S : assigned(S, red) }.

% One team has 2, the other has 3
:- team_size(green, N1), team_size(red, N2), N1 + N2 != 5.
:- team_size(green, N1), N1 != 2, N1 != 3.
:- team_size(red, N2), N2 != 2, N2 != 3.

% One facilitator per team - facilitator must be on that team
1 { facilitator(S, T) : assigned(S, T) } 1 :- team(T).

% Constraint 1: Juana and Olga on different teams
:- assigned(juana, T), assigned(olga, T).

% Constraint 2: Lateefah on green team
assigned(lateefah, green).

% Constraint 3: Kelly is not a facilitator
:- facilitator(kelly, _).

% Constraint 4: Olga is a facilitator
:- not is_facilitator(olga).

% Helper: check if a student is a facilitator
is_facilitator(S) :- facilitator(S, _).

% Evaluate answer choices

% (A) Juana is assigned to the red team
a_holds :- assigned(juana, red).
a_fails :- assigned(juana, green).

% (B) Lateefah is a facilitator
b_holds :- is_facilitator(lateefah).
b_fails :- assigned(lateefah, T), not facilitator(lateefah, T).

% (C) Olga is assigned to the green team
c_holds :- assigned(olga, green).
c_fails :- assigned(olga, red).

% (D) Juana and Mei are not both facilitators
both_juana_mei :- is_facilitator(juana), is_facilitator(mei).
d_holds :- not both_juana_mei.
d_fails :- both_juana_mei.

% (E) Neither Juana nor Kelly is a facilitator
e_holds :- not is_facilitator(juana), not is_facilitator(kelly).
e_fails :- is_facilitator(juana).
e_fails :- is_facilitator(kelly).

% An answer "must be true" if it holds in ALL models
option(a) :- a_holds, not a_fails.
option(b) :- b_holds, not b_fails.
option(c) :- c_holds, not c_fails.
option(d) :- d_holds, not d_fails.
option(e) :- e_holds, not e_fails.

#show option/1.
#show assigned/2.
#show facilitator/2.
#show a_holds/0.
#show b_holds/0.
#show c_holds/0.
#show d_holds/0.
#show e_holds/0.
#show a_fails/0.
#show b_fails/0.
#show c_fails/0.
#show d_fails/0.
#show e_fails/0.