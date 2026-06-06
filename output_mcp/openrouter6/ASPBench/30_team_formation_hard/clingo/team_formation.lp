% =====================
% Personnel Data
% =====================
person(alex). person(ben). person(chloe). person(david). person(grace). person(harry).
person(eva). person(frank). person(ivy). person(jack). person(kate). person(leo).

level(alex, senior). level(ben, senior). level(chloe, senior). level(david, senior).
level(grace, senior). level(harry, senior). level(eva, junior). level(frank, junior).
level(ivy, junior). level(jack, junior). level(kate, junior). level(leo, junior).

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

% Incompatibilities
incompatible(alex, ben). incompatible(chloe, grace). incompatible(david, harry).

% Synergy pairs
synergy_pair(programming, devops).
synergy_pair(design, datascience).
synergy_pair(management, testing).
synergy_pair(security, cloud).

% Projects and requirements
project(alpha). project(beta). project(gamma).
project_requirement(alpha, security).
project_requirement(beta, cloud).

% Primary skills (for leaders)
primary_skill(programming). primary_skill(design). primary_skill(testing).
primary_skill(management). primary_skill(datascience). primary_skill(devops).

% Teams
team(1). team(2). team(3).

% =====================
% Decision Variables
% =====================

% Each person assigned to exactly one team
1 { team_member(T, P) : team(T) } 1 :- person(P).

% Each team has exactly 4 members
4 { team_member(T, P) : person(P) } 4 :- team(T).

% Each team assigned to exactly one project (bijection)
1 { team_project(T, P) : project(P) } 1 :- team(T).
1 { team_project(T, P) : team(T) } 1 :- project(P).

% Each team has exactly one leader (senior)
1 { team_leader(T, P) : person(P), level(P, senior) } 1 :- team(T).

% Leader must be a member of the team
:- team_leader(T, P), not team_member(T, P).

% Leader's primary skill (exactly one per team, must be a skill of the leader)
1 { leader_primary_skill(T, S) : has_skill(P, S), primary_skill(S) } 1 :- team_leader(T, P).

% Primary skills must be distinct across teams
:- leader_primary_skill(T1, S), leader_primary_skill(T2, S), T1 != T2.

% =====================
% Constraints
% =====================

% Incompatibilities: cannot be on same team
:- team_member(T, P1), team_member(T, P2), incompatible(P1, P2).

% Project requirements
has_skill_in_team(T, S) :- team_member(T, P), has_skill(P, S).
:- team_project(T, alpha), not has_skill_in_team(T, security).
:- team_project(T, beta), not has_skill_in_team(T, cloud).

% =====================
% Synergy Score Calculation
% =====================

% For each team, count synergy pairs present
synergy_score(T, N) :- team(T), N = #count { S1, S2 : synergy_pair(S1, S2), has_skill_in_team(T, S1), has_skill_in_team(T, S2) }.

% Total synergy (to be maximized)
total_synergy(S) :- S = #sum { N, T : synergy_score(T, N) }.

% =====================
% Output Formatting
% =====================

% Team output with members (unsorted for simplicity)
team_output(T, Project, Leader, Score) :-
    team(T), team_project(T, Project), team_leader(T, Leader), synergy_score(T, Score).

% Show the required output
#show team_output/4.
#show total_synergy/1.

% =====================
% Optimization
% =====================
#maximize { N, T : synergy_score(T, N) }.