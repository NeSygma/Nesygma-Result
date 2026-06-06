% Define people and skills
person(alice; bob; carol; dave; eve; frank; grace; henry).
skill(programming; design; testing; management; documentation).

% Define which person has which skill
has_skill(alice, programming).
has_skill(alice, design).
has_skill(bob, programming).
has_skill(bob, testing).
has_skill(carol, design).
has_skill(carol, management).
has_skill(dave, testing).
has_skill(dave, management).
has_skill(eve, programming).
has_skill(eve, documentation).
has_skill(frank, design).
has_skill(frank, documentation).
has_skill(grace, testing).
has_skill(grace, documentation).
has_skill(henry, management).
has_skill(henry, documentation).

% Define required skills for team formation
required_skill(programming; design; testing; management).

% Define teams (2 teams)
team(1..2).

% Assign each person to exactly one team
{ assigned(P, T) : team(T) } = 1 :- person(P).

% Each team must have exactly 4 people
:- team(T), #count { P : assigned(P, T) } != 4.

% Each team must have at least one person with each required skill
has_team_skill(T, S) :- assigned(P, T), has_skill(P, S), required_skill(S).
:- team(T), required_skill(S), not has_team_skill(T, S).

% Objective: Minimize skill overlap within teams
% For each team and skill, count the number of people with that skill
team_skill_count(T, S, N) :- 
    team(T), 
    required_skill(S), 
    N = #count { P : assigned(P, T), has_skill(P, S) }.

% For each team, find the maximum count of any skill
team_max_skill(T, Max) :- 
    team(T), 
    Max = #max { N : team_skill_count(T, S, N) }.

% Minimize the sum of the maximum skill counts across teams
#minimize { Max : team_max_skill(_, Max) }.

% Show the assignment
#show assigned/2.
#show team_max_skill/2.