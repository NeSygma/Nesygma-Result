% Team Formation Problem
% Form 2 teams of 4 people each with required skills

% People
people(alice). people(bob). people(carol). people(dave).
people(eve). people(frank). people(grace). people(henry).

% Skills
skills(programming). skills(design). skills(testing). skills(management). skills(documentation).

% Required skills (must be covered by each team)
required_skill(programming). required_skill(design). required_skill(testing). required_skill(management).

% Person skills
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

% Teams
team(1). team(2).

% Assignment: each person to exactly one team
1 { assignment(Person, Team) : team(Team) } 1 :- people(Person).

% Each team must have exactly 4 people
:- team(T), N = #count{ P : assignment(P, T) }, N != 4.

% Each team must have at least one person with each required skill
has_skill_in_team(T, S) :- assignment(P, T), has_skill(P, S).
:- team(T), required_skill(S), not has_skill_in_team(T, S).

% Count of people with each required skill in each team
count_skill(T, S, N) :- team(T), required_skill(S), N = #count{ P : assignment(P, T), has_skill(P, S) }.

% Overlap for each skill in each team (N-1)
overlap(T, S, O) :- count_skill(T, S, N), O = N - 1.

% Minimize total overlap (skill duplication within teams)
#minimize { O : overlap(T, S, O) }.

% Symmetry breaking: Alice in team 1
assignment(alice, 1).

% Output: team members
team1_member(P) :- assignment(P, 1).
team2_member(P) :- assignment(P, 2).

#show assignment/2.
#show team1_member/1.
#show team2_member/1.