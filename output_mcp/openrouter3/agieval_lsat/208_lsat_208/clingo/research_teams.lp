% Students
student(juana).
student(kelly).
student(lateefah).
student(mei).
student(olga).

% Teams
team(green).
team(red).

% Domain: each student assigned to exactly one team
1 { assigned(Student, Team) : team(Team) } 1 :- student(Student).

% Each team has exactly one facilitator
1 { facilitator(Student, Team) : student(Student) } 1 :- team(Team).

% Constraint: Juana is assigned to a different team than Olga
:- assigned(juana, Team), assigned(olga, Team).

% Constraint: Lateefah is assigned to the green team
:- not assigned(lateefah, green).

% Constraint: Kelly is not a facilitator
:- facilitator(kelly, Team).

% Constraint: Olga is a facilitator
:- not facilitator(olga, Team).

% Team size constraints: one team has 2 members, the other has 3 members
% Count members per team
member_count(Team, Count) :- team(Team), Count = #count{Student : assigned(Student, Team)}.
% One team has 2, the other has 3
:- member_count(green, N), member_count(red, M), not (N = 2, M = 3), not (N = 3, M = 2).

% Helper predicates for each option
% Option A: green team: Juana, Lateefah, Olga (facilitator); red team: Kelly, Mei (facilitator)
option_a :-
    assigned(juana, green), assigned(lateefah, green), assigned(olga, green),
    assigned(kelly, red), assigned(mei, red),
    facilitator(olga, green), facilitator(mei, red),
    not facilitator(juana, green), not facilitator(lateefah, green),
    not facilitator(kelly, red), not facilitator(juana, red), not facilitator(lateefah, red), not facilitator(olga, red), not facilitator(mei, green).

% Option B: green team: Kelly, Lateefah (facilitator), Olga; red team: Juana, Mei (facilitator)
option_b :-
    assigned(kelly, green), assigned(lateefah, green), assigned(olga, green),
    assigned(juana, red), assigned(mei, red),
    facilitator(lateefah, green), facilitator(mei, red),
    not facilitator(kelly, green), not facilitator(olga, green),
    not facilitator(juana, red), not facilitator(kelly, red), not facilitator(lateefah, red), not facilitator(olga, red), not facilitator(mei, green).

% Option C: green team: Kelly, Lateefah, Olga (facilitator); red team: Juana (facilitator), Mei
option_c :-
    assigned(kelly, green), assigned(lateefah, green), assigned(olga, green),
    assigned(juana, red), assigned(mei, red),
    facilitator(olga, green), facilitator(juana, red),
    not facilitator(kelly, green), not facilitator(lateefah, green),
    not facilitator(mei, red), not facilitator(kelly, red), not facilitator(lateefah, red), not facilitator(olga, red), not facilitator(juana, green), not facilitator(mei, green).

% Option D: green team: Kelly, Mei, Olga (facilitator); red team: Juana (facilitator), Lateefah
option_d :-
    assigned(kelly, green), assigned(mei, green), assigned(olga, green),
    assigned(juana, red), assigned(lateefah, red),
    facilitator(olga, green), facilitator(juana, red),
    not facilitator(kelly, green), not facilitator(mei, green),
    not facilitator(lateefah, red), not facilitator(kelly, red), not facilitator(mei, red), not facilitator(olga, red), not facilitator(juana, green), not facilitator(lateefah, green).

% Option E: green team: Lateefah, Olga (facilitator); red team: Juana, Kelly (facilitator), Mei
option_e :-
    assigned(lateefah, green), assigned(olga, green),
    assigned(juana, red), assigned(kelly, red), assigned(mei, red),
    facilitator(olga, green), facilitator(kelly, red),
    not facilitator(lateefah, green),
    not facilitator(juana, red), not facilitator(mei, red), not facilitator(lateefah, red), not facilitator(olga, red), not facilitator(juana, green), not facilitator(kelly, green), not facilitator(mei, green).

% Map the correct answer to option/1 (MANDATORY)
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.