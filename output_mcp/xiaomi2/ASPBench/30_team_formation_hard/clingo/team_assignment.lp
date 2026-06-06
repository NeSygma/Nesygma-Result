% Team Assignment Problem - ASP Model

% ==================== DOMAINS ====================
% Personnel
person(alex). person(ben). person(chloe). person(david). person(grace). person(harry).
person(eva). person(frank). person(ivy). person(jack). person(kate). person(leo).

% Levels
senior(alex). senior(ben). senior(chloe). senior(david). senior(grace). senior(harry).
junior(eva). junior(frank). junior(ivy). junior(jack). junior(kate). junior(leo).

% Skills
has_skill(alex, programming). has_skill(alex, security).
has_skill(ben, programming). has_skill(ben, devops).
has_skill(chloe, design). has_skill(chloe, management).
has_skill(david, testing). has_skill(david, datascience).
has_skill(grace, management). has_skill(grace, datascience).
has_skill(harry, devops). has_skill(harry, security).
has_skill(eva, programming). has_skill(eva, cloud).
has_skill(frank, design). has_skill(frank, testing).
has_skill(ivy, design). has_skill(ivy, cloud).
has_skill(jack, testing). has_skill(jack, programming).
has_skill(kate, management). has_skill(kate, devops).
has_skill(leo, datascience). has_skill(leo, security).

% Primary skills (for leader constraint)
primary_skill(programming). primary_skill(design). primary_skill(testing).
primary_skill(management). primary_skill(datascience). primary_skill(devops).

% Projects
project(alpha). project(beta). project(gamma).

% Project requirements
requires(alpha, security).
requires(beta, cloud).
% gamma has no requirement

% Incompatibilities
incompatible(alex, ben).
incompatible(chloe, grace).
incompatible(david, harry).
% Make symmetric
incompatible(X, Y) :- incompatible(Y, X).

% Synergy pairs
synergy_pair(programming, devops).
synergy_pair(design, datascience).
synergy_pair(management, testing).
synergy_pair(security, cloud).

% Teams
team(1). team(2). team(3).

% ==================== DECISION VARIABLES ====================
% Assign each person to exactly one team
1 { assigned(P, T) : team(T) } 1 :- person(P).

% Assign each team to exactly one project
1 { project_assigned(T, P) : project(P) } 1 :- team(T).

% Each team has exactly one leader (must be senior)
1 { leader(T, P) : person(P), senior(P) } 1 :- team(T).

% Leader must be assigned to their team
:- leader(T, P), not assigned(P, T).

% ==================== CONSTRAINTS ====================
% Each team has exactly 4 members
4 { assigned(P, T) : person(P) } 4 :- team(T).

% Incompatibility constraint: incompatible persons cannot be on same team
:- assigned(P1, T), assigned(P2, T), incompatible(P1, P2).

% Project requirements: team must have required skill
:- project_assigned(T, alpha), not has_skill_in_team(T, security).
:- project_assigned(T, beta), not has_skill_in_team(T, cloud).

% Helper: team has a skill if any member has it
has_skill_in_team(T, S) :- assigned(P, T), has_skill(P, S).

% Leader primary skills must be mutually exclusive
:- leader(T1, P1), leader(T2, P2), T1 != T2,
   has_skill(P1, S), has_skill(P2, S), primary_skill(S).

% ==================== SYNERGY CALCULATION ====================
% Team has synergy pair if it has both skills
team_has_synergy(T, S1, S2) :- 
    synergy_pair(S1, S2),
    has_skill_in_team(T, S1),
    has_skill_in_team(T, S2).

% Count synergy points per team
team_synergy_score(T, N) :- 
    team(T),
    N = #count { S1, S2 : team_has_synergy(T, S1, S2) }.

% Total synergy
total_synergy(S) :- 
    S = #sum { N, T : team_synergy_score(T, N) }.

% ==================== OUTPUT ====================
#show assigned/2.
#show project_assigned/2.
#show leader/2.
#show team_synergy_score/2.
#show total_synergy/1.

% Maximize total synergy
#maximize { S : total_synergy(S) }.