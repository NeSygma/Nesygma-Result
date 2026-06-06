% Define the students and teams
student(juana; kelly; lateefah; mei; olga).
team(green; red).
role(member; facilitator).

% Assign each student to exactly one team
1 { assigned_to(Student, Team) : team(Team) } 1 :- student(Student).

% Assign each student to exactly one role
1 { has_role(Student, Role) : role(Role) } 1 :- student(Student).

% Lateefah is assigned to the green team
:- not assigned_to(lateefah, green).

% Juana is assigned to a different team than Olga
:- assigned_to(juana, Team), assigned_to(olga, Team).

% Kelly is not a facilitator
:- has_role(kelly, facilitator).

% Olga is a facilitator
:- not has_role(olga, facilitator).

% Ensure one team has 2 members and the other has 3
:- team(Team), { assigned_to(Student, Team) : student(Student) } != 2, { assigned_to(Student, Team) : student(Student) } != 3.

% Ensure exactly one facilitator per team
:- team(Team), { has_role(Student, facilitator) : assigned_to(Student, Team) } != 1.

% Define the answer choices as possible assignments
% Choice A: green team: Juana, Lateefah, Olga (facilitator); red team: Kelly, Mei (facilitator)
answer(a) :-
    assigned_to(juana, green),
    assigned_to(lateefah, green),
    assigned_to(olga, green),
    assigned_to(kelly, red),
    assigned_to(mei, red),
    has_role(olga, facilitator),
    has_role(mei, facilitator),
    has_role(juana, member),
    has_role(lateefah, member),
    has_role(kelly, member).

% Choice B: green team: Kelly, Lateefah (facilitator), Olga; red team: Juana, Mei (facilitator)
answer(b) :-
    assigned_to(kelly, green),
    assigned_to(lateefah, green),
    assigned_to(olga, green),
    assigned_to(juana, red),
    assigned_to(mei, red),
    has_role(lateefah, facilitator),
    has_role(mei, facilitator),
    has_role(olga, member),
    has_role(kelly, member),
    has_role(juana, member).

% Choice C: green team: Kelly, Lateefah, Olga (facilitator); red team: Juana (facilitator), Mei
answer(c) :-
    assigned_to(kelly, green),
    assigned_to(lateefah, green),
    assigned_to(olga, green),
    assigned_to(juana, red),
    assigned_to(mei, red),
    has_role(olga, facilitator),
    has_role(juana, facilitator),
    has_role(kelly, member),
    has_role(lateefah, member),
    has_role(mei, member).

% Choice D: green team: Kelly, Mei, Olga (facilitator); red team: Juana (facilitator), Lateefah
answer(d) :-
    assigned_to(kelly, green),
    assigned_to(mei, green),
    assigned_to(olga, green),
    assigned_to(juana, red),
    assigned_to(lateefah, red),
    has_role(olga, facilitator),
    has_role(juana, facilitator),
    has_role(kelly, member),
    has_role(mei, member),
    has_role(lateefah, member).

% Choice E: green team: Lateefah, Olga (facilitator); red team: Juana, Kelly (facilitator), Mei
answer(e) :-
    assigned_to(lateefah, green),
    assigned_to(olga, green),
    assigned_to(juana, red),
    assigned_to(kelly, red),
    assigned_to(mei, red),
    has_role(olga, facilitator),
    has_role(kelly, facilitator),
    has_role(juana, member),
    has_role(lateefah, member),
    has_role(mei, member).

% Map the correct answer to option/1
option(a) :- answer(a).
option(b) :- answer(b).
option(c) :- answer(c).
option(d) :- answer(d).
option(e) :- answer(e).

#show option/1.