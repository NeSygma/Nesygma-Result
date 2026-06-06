% Facts
person(alex). person(ben). person(chloe). person(david). person(grace). person(harry). person(eva). person(frank). person(ivy). person(jack). person(kate). person(leo).

level(alex, senior). level(ben, senior). level(chloe, senior). level(david, senior). level(grace, senior). level(harry, senior).
level(eva, junior). level(frank, junior). level(ivy, junior). level(jack, junior). level(kate, junior). level(leo, junior).

skill(alex, programming). skill(alex, security).
skill(ben, programming). skill(ben, devops).
skill(chloe, design). skill(chloe, management).
skill(david, testing). skill(david, datasci).
skill(grace, management). skill(grace, datasci).
skill(harry, devops). skill(harry, security).
skill(eva, programming). skill(eva, cloud).
skill(frank, design). skill(frank, testing).
skill(ivy, design). skill(ivy, cloud).
skill(jack, testing). skill(jack, programming).
skill(kate, management). skill(kate, devops).
skill(leo, datasci). skill(leo, security).

synergy_pair(programming, devops). synergy_pair(design, datasci). synergy_pair(management, testing). synergy_pair(security, cloud).

incompatibility(alex, ben). incompatibility(ben, alex). incompatibility(chloe, grace). incompatibility(grace, chloe). incompatibility(david, harry). incompatibility(harry, david).

project_name(alpha). project_name(beta). project_name(gamma).
project_requirement(alpha, security). project_requirement(beta, cloud).

team(1). team(2). team(3).

% Primary skill choice for each person
{ primary_skill(P,S) : skill(P,S) } 1 :- person(P).

% Assignment of each person to exactly one team
1 { assign(P,T) : team(T) } 1 :- person(P).

% Each team has exactly 4 members
4 { assign(P,T) : person(P) } 4 :- team(T).

% Each team has exactly one senior leader
1 { leader(T,P) : assign(P,T), level(P, senior) } 1 :- team(T).

% Leaders must have distinct primary skills
:- leader(T1,P1), leader(T2,P2), T1 != T2, primary_skill(P1,S), primary_skill(P2,S).

% Incompatibilities cannot be on same team
:- assign(P1,T), assign(P2,T), incompatibility(P1,P2).

% Project assignment for each team
1 { project(T,Proj) : project_name(Proj) } 1 :- team(T).

% No duplicate projects
:- project(T1,Proj), project(T2,Proj), T1 != T2.

% Project requirements
:- project(T,Proj), project_requirement(Proj,Skill), not has_skill(T,Skill).

% Team has a skill if any member has it
has_skill(T,Skill) :- assign(P,T), skill(P,Skill).

% Synergy score per team
synergy_score(T,S) :- team(T), S = #count{1 : synergy_pair(S1,S2), has_skill(T,S1), has_skill(T,S2)}.

% Objective: maximize total synergy
#maximize { S : synergy_score(T,S) }.

% Show relevant atoms
#show assign/2.
#show leader/2.
#show project/2.
#show synergy_score/2.
#show total_synergy/1.