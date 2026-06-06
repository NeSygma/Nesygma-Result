%% Problem: Form 2 teams of 4 people each with skill coverage

%% People
person(alice; bob; carol; dave; eve; frank; grace; henry).

%% Required skills
required_skill(programming; design; testing; management).

%% Skills per person
skill(alice, programming).
skill(alice, design).
skill(bob, programming).
skill(bob, testing).
skill(carol, design).
skill(carol, management).
skill(dave, testing).
skill(dave, management).
skill(eve, programming).
skill(eve, documentation).
skill(frank, design).
skill(frank, documentation).
skill(grace, testing).
skill(grace, documentation).
skill(henry, management).
skill(henry, documentation).

%% Teams: team(1) and team(2)
team(1..2).

%% Each person assigned to exactly one team
1 { assigned(P, T) : team(T) } 1 :- person(P).

%% Each team has exactly 4 people
:- team(T), #count { P : assigned(P, T) } != 4.

%% Each team must have at least one person with each required skill
:- team(T), required_skill(S), not assigned(P, T) : skill(P, S).

%% Minimize skill overlap within teams:
%% For each team and each skill, count how many people have that skill.
%% We want to minimize the sum over teams of (count - 1) for each skill,
%% i.e., penalize extra people with the same skill beyond the first.
%% Equivalent: minimize sum over teams of (#people with skill in team - 1) for each skill.
%% Which is same as: minimize sum over teams of (#people with skill in team) for each skill,
%% since the -1 per skill per team is constant (4 skills * 2 teams = 8 constant).
%% So we minimize total skill occurrences across teams.

#minimize { 1, P, T, S : assigned(P, T), skill(P, S) }.

%% Show the result
#show assigned/2.