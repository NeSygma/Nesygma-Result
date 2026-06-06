% Team Formation Problem - Clingo ASP Model

% ===== DOMAIN DEFINITIONS =====
% Personnel
person("Alex"). person("Ben"). person("Chloe"). person("David").
person("Grace"). person("Harry"). person("Eva"). person("Frank").
person("Ivy"). person("Jack"). person("Kate"). person("Leo").

% Levels
level("Alex", senior). level("Ben", senior). level("Chloe", senior).
level("David", senior). level("Grace", senior). level("Harry", senior).
level("Eva", junior). level("Frank", junior). level("Ivy", junior).
level("Jack", junior). level("Kate", junior). level("Leo", junior).

% Skills for each person
skill("Alex", programming). skill("Alex", security).
skill("Ben", programming). skill("Ben", devops).
skill("Chloe", design). skill("Chloe", management).
skill("David", testing). skill("David", datascience).
skill("Grace", management). skill("Grace", datascience).
skill("Harry", devops). skill("Harry", security).
skill("Eva", programming). skill("Eva", cloud).
skill("Frank", design). skill("Frank", testing).
skill("Ivy", design). skill("Ivy", cloud).
skill("Jack", testing). skill("Jack", programming).
skill("Kate", management). skill("Kate", devops).
skill("Leo", datascience). skill("Leo", security).

% Primary skills (for leader exclusivity)
primary_skill(programming). primary_skill(design). primary_skill(testing).
primary_skill(management). primary_skill(datascience). primary_skill(devops).

% Projects
project("Alpha"). project("Beta"). project("Gamma").

% Project requirements
requires("Alpha", security).
requires("Beta", cloud).
% Gamma has no specific requirement

% Incompatibilities
incompatible("Alex", "Ben"). incompatible("Ben", "Alex").
incompatible("Chloe", "Grace"). incompatible("Grace", "Chloe").
incompatible("David", "Harry"). incompatible("Harry", "David").

% Synergy pairs
synergy_pair(programming, devops).
synergy_pair(design, datascience).
synergy_pair(management, testing).
synergy_pair(security, cloud).

% Teams
team(1). team(2). team(3).

% ===== TEAM ASSIGNMENT =====
% Each person assigned to exactly one team
1 { member(T, P) : team(T) } 1 :- person(P).

% Each team has exactly 4 members
4 { member(T, P) : person(P) } 4 :- team(T).

% ===== PROJECT ASSIGNMENT =====
% Each team assigned to exactly one project
1 { assigned_project(T, P) : project(P) } 1 :- team(T).

% Each project assigned to exactly one team
1 { assigned_project(T, P) : team(T) } 1 :- project(P).

% ===== LEADER SELECTION =====
% Each team has exactly one leader (must be senior)
1 { leader(T, P) : person(P), level(P, senior) } 1 :- team(T).

% Leader must be a member of the team
:- leader(T, P), not member(T, P).

% ===== LEADER SKILL EXCLUSIVITY =====
% Each leader must have a unique primary skill
% Define which primary skill each leader has
leader_has_skill(T, P, Skill) :- leader(T, P), skill(P, Skill), primary_skill(Skill).

% Leaders must have mutually exclusive primary skills
% No two leaders can share the same primary skill
:- leader(T1, P1), leader(T2, P2), T1 != T2,
   leader_has_skill(T1, P1, S), leader_has_skill(T2, P2, S).

% ===== INCOMPATIBILITY CONSTRAINTS =====
% Incompatible people cannot be on the same team
:- member(T, P1), member(T, P2), incompatible(P1, P2).

% ===== PROJECT REQUIREMENTS =====
% Teams must satisfy project skill requirements
% For each team and project, check if required skills are present
has_skill(T, Skill) :- member(T, P), skill(P, Skill).

% Alpha requires security
:- assigned_project(T, "Alpha"), not has_skill(T, security).

% Beta requires cloud
:- assigned_project(T, "Beta"), not has_skill(T, cloud).

% ===== SYNERGY CALCULATION =====
% Calculate synergy score for each team
% A team gets a point for each synergy pair where both skills are present
team_synergy(T, Score) :-
    team(T),
    Score = #count{ S1, S2 : synergy_pair(S1, S2), has_skill(T, S1), has_skill(T, S2) }.

% Total synergy across all teams
total_synergy(S) :-
    S = #sum{ Score, T : team_synergy(T, Score) }.

% ===== OPTIMIZATION =====
% Maximize total synergy
#maximize { S : total_synergy(S) }.

% ===== OUTPUT =====
% Show the solution
#show team/1.
#show member/2.
#show leader/2.
#show assigned_project/2.
#show team_synergy/2.
#show total_synergy/1.