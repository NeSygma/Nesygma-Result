% --- Data ---
person(alex, senior). person(ben, senior). person(chloe, senior).
person(david, senior). person(grace, senior). person(harry, senior).
person(eva, junior). person(frank, junior). person(ivy, junior).
person(jack, junior). person(kate, junior). person(leo, junior).

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

project(alpha, security).
project(beta, cloud).
project(gamma, none).

incompatible(alex, ben).
incompatible(chloe, grace).
incompatible(david, harry).

synergy_pair(programming, devops).
synergy_pair(design, datascience).
synergy_pair(management, testing).
synergy_pair(security, cloud).

team(1..3).

% --- Constraints ---

% 1. Assignment: Each person assigned to exactly one team
{ assign(P, T) : team(T) } = 1 :- person(P, _).

% 2. Team Size: Each team must have exactly 4 members
:- team(T), not #count { P : assign(P, T) } = 4.

% 3. Projects: Each team assigned to exactly one project
{ team_project(T, P) : project(P, _) } = 1 :- team(T).
:- project(P, _), not #count { T : team_project(T, P) } = 1.

% 4. Leadership: Each team has exactly one leader who must be Senior level
{ leader(T, P) : assign(P, T), person(P, senior) } = 1 :- team(T).

% 5. Leader Skills: Team leaders must have mutually exclusive primary skills
% (A leader might have multiple skills, so we check if any skill is shared)
leader_skill(T, S) :- leader(T, P), has_skill(P, S).
:- leader_skill(T1, S), leader_skill(T2, S), T1 != T2.

% 6. Incompatibilities: Cannot be on the same team
:- assign(P1, T), assign(P2, T), incompatible(P1, P2).

% 7. Project Requirements: Teams must satisfy the skill requirements
team_has_skill(T, S) :- assign(P, T), has_skill(P, S).
:- team_project(T, P), project(P, Req), Req != none, not team_has_skill(T, Req).

% --- Objective ---
team_synergy(T, S1, S2) :- synergy_pair(S1, S2), team_has_skill(T, S1), team_has_skill(T, S2).
score(T, N) :- team(T), N = #count { S1, S2 : team_synergy(T, S1, S2) }.
total_score(S) :- S = #sum { N, T : score(T, N) }.

#maximize { S : total_score(S) }.

% --- Output ---
#show assign/2.
#show team_project/2.
#show leader/2.
#show total_score/1.