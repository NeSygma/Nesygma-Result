% Domains
person(alex; ben; chloe; david; grace; harry; eva; frank; ivy; jack; kate; leo).
level(senior; junior).
skill(programming; security; devops; design; management; datascience; testing; cloud).
project(alpha; beta; gamma).
team(team1; team2; team3).

% Personnel facts: person(Name, Level, [Skills])
has_skill(alex, programming).
has_skill(alex, security).
has_skill(alex, senior).
has_skill(ben, programming).
has_skill(ben, devops).
has_skill(ben, senior).
has_skill(chloe, design).
has_skill(chloe, management).
has_skill(chloe, senior).
has_skill(david, testing).
has_skill(david, datascience).
has_skill(david, senior).
has_skill(grace, management).
has_skill(grace, datascience).
has_skill(grace, senior).
has_skill(harry, devops).
has_skill(harry, security).
has_skill(harry, senior).
has_skill(eva, programming).
has_skill(eva, cloud).
has_skill(eva, junior).
has_skill(frank, design).
has_skill(frank, testing).
has_skill(frank, junior).
has_skill(ivy, design).
has_skill(ivy, cloud).
has_skill(ivy, junior).
has_skill(jack, testing).
has_skill(jack, programming).
has_skill(jack, junior).
has_skill(kate, management).
has_skill(kate, devops).
has_skill(kate, junior).
has_skill(leo, datascience).
has_skill(leo, security).
has_skill(leo, junior).

% Project requirements
project_requirement(alpha, security).
project_requirement(beta, cloud).
% Gamma has no specific requirement

% Incompatibilities
incompatible(alex, ben).
incompatible(ben, alex).
incompatible(chloe, grace).
incompatible(grace, chloe).
incompatible(david, harry).
incompatible(harry, david).

% Synergy pairs
synergy_pair(programming, devops).
synergy_pair(devops, programming).
synergy_pair(design, datascience).
synergy_pair(datascience, design).
synergy_pair(management, testing).
synergy_pair(testing, management).
synergy_pair(security, cloud).
synergy_pair(cloud, security).

% Senior personnel
senior(alex; ben; chloe; david; grace; harry).

% Team assignment and leadership
% Each person assigned to exactly one team
1 { assigned_team(P, T) : team(T) } 1 :- person(P).

% Each team has exactly 4 members
:- team(T), #count { P : assigned_team(P, T) } != 4.

% Each team has exactly one Senior leader
1 { team_leader(T, P) : senior(P) } 1 :- team(T).

% Leader must be assigned to their own team
:- team_leader(T, P), not assigned_team(P, T).

% Leaders must have mutually exclusive primary skills
% Get the skills of each leader and ensure no overlap in primary skills
leader_skill(T, S) :- team_leader(T, P), has_skill(P, S).

% Constraint: No two leaders can share a skill
:- leader_skill(T1, S), leader_skill(T2, S), T1 != T2.

% Incompatibility constraint: incompatible people cannot be on same team
:- assigned_team(P1, T), assigned_team(P2, T), incompatible(P1, P2).

% Project assignment: each team assigned to exactly one project
1 { team_project(T, P) : project(P) } 1 :- team(T).

% Project requirement satisfaction
% For teams assigned to Alpha (requires security), at least one member must have security skill
:- team_project(T, alpha), not has_security(T).
has_security(T) :- assigned_team(P, T), has_skill(P, security).

% For teams assigned to Beta (requires cloud), at least one member must have cloud skill
:- team_project(T, beta), not has_cloud(T).
has_cloud(T) :- assigned_team(P, T), has_skill(P, cloud).

% Synergy calculation for each team
% A synergy point is awarded for each synergy_pair present among team members
% We'll count the number of synergy pairs in each team

% Helper: team_has_skill_pair(T, S1, S2) if team T has both S1 and S2
% Ensure P1 and P2 are distinct
team_has_skill_pair(T, S1, S2) :-
    assigned_team(P1, T), has_skill(P1, S1),
    assigned_team(P2, T), has_skill(P2, S2),
    synergy_pair(S1, S2),
    P1 != P2.

% Count synergy pairs per team
team_synergy(T, N) :- team(T), N = #count { S1, S2 : team_has_skill_pair(T, S1, S2) }.

% Calculate total synergy
#sum { N, T : team_synergy(T, N) } = TotalSynergy.

% Objective: maximize total synergy
#maximize { TotalSynergy }.

% Show the solution
#show team_leader/2.
#show team_project/2.
#show assigned_team/2.
#show team_synergy/2.
#show TotalSynergy.