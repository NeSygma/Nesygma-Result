% Persons
person(alice). person(bob). person(carol). person(dave). person(eve). person(frank). person(grace). person(henry).

% Skills
skill(alice, programming). skill(alice, design).
skill(bob, programming). skill(bob, testing).
skill(carol, design). skill(carol, management).
skill(dave, testing). skill(dave, management).
skill(eve, programming). skill(eve, documentation).
skill(frank, design). skill(frank, documentation).
skill(grace, testing). skill(grace, documentation).
skill(henry, management). skill(henry, documentation).

% Required skills
required_skill(programming). required_skill(design). required_skill(testing). required_skill(management).

% Team identifiers
team_id(1). team_id(2).

% Each person assigned to exactly one team
1 { team(Team, Person) : team_id(Team) } 1 :- person(Person).

% Each team has exactly 4 members
4 { team(Team, Person) : person(Person) } 4 :- team_id(Team).

% Each team must have at least one of each required skill
team_has_skill(Team, Skill) :- team(Team, Person), skill(Person, Skill), required_skill(Skill).
:- team_id(Team), required_skill(Skill), not team_has_skill(Team, Skill).

% Overlap flag: true if more than one person in team has same skill
overlap_flag(Team, Skill) :- #count{ Person : team(Team, Person), skill(Person, Skill) } > 1.

% Minimize number of overlapping skill instances
#minimize { 1 : overlap_flag(Team, Skill) }.

#show team/2.