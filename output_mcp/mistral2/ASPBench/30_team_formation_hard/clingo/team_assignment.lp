% --- Facts: Personnel ---
person(alex; ben; chloe; david; grace; harry; eva; frank; ivy; jack; kate; leo).

senior(alex; ben; chloe; david; grace; harry).
junior(eva; frank; ivy; jack; kate; leo).

skill(alex, "programming").
skill(alex, "security").
skill(ben, "programming").
skill(ben, "devops").
skill(chloe, "design").
skill(chloe, "management").
skill(david, "testing").
skill(david, "datascience").
skill(grace, "management").
skill(grace, "datascience").
skill(harry, "devops").
skill(harry, "security").
skill(eva, "programming").
skill(eva, "cloud").
skill(frank, "design").
skill(frank, "testing").
skill(ivy, "design").
skill(ivy, "cloud").
skill(jack, "testing").
skill(jack, "programming").
skill(kate, "management").
skill(kate, "devops").
skill(leo, "datascience").
skill(leo, "security").

% --- Facts: Projects ---
project(alpha; beta; gamma).

project_requirement(alpha, "security").
project_requirement(beta, "cloud").

% --- Facts: Synergy Pairs ---
synergy_pair("programming", "devops").
synergy_pair("design", "datascience").
synergy_pair("management", "testing").
synergy_pair("security", "cloud").

% --- Facts: Incompatibilities ---
incompatible(alex, ben).
incompatible(ben, alex).
incompatible(chloe, grace).
incompatible(grace, chloe).
incompatible(david, harry).
incompatible(harry, david).

% --- Domains ---
team(1..3).

% --- Assign each person to exactly one team ---
1 { assigned(P, T) : team(T) } 1 :- person(P).

% --- Each team has exactly 4 members ---
:- team(T), #count { P : assigned(P, T) } != 4.

% --- Leadership: Each team has exactly one leader, who must be Senior ---
1 { leader(T, P) : senior(P) } 1 :- team(T).

% --- Leaders must be assigned to their team ---
:- leader(T, P), not assigned(P, T).

% --- Leaders must have mutually exclusive primary skills ---
% Primary skill is the first skill listed for each person.
primary_skill(P, S) :- skill(P, S), senior(P).

% No two leaders can share a primary skill.
:- leader(T1, P1), leader(T2, P2), T1 < T2, primary_skill(P1, S), primary_skill(P2, S).

% --- Project Assignment: Each team assigned to exactly one project ---
1 { project_assignment(T, P) : project(P) } 1 :- team(T).

% No two teams can be assigned to the same project ---
:- project(P), 2 { T : project_assignment(T, P) }.

% --- Project Requirements ---
% Team assigned to alpha must have at least one member with "security" skill.
:- project_assignment(T, alpha), not has_required_skill(T, "security").

% Team assigned to beta must have at least one member with "cloud" skill.
:- project_assignment(T, beta), not has_required_skill(T, "cloud").

% Gamma has no requirement, so no constraint.

% Helper: Check if a team has a required skill.
has_required_skill(T, Skill) :-
    assigned(P, T),
    skill(P, Skill).

% --- Incompatibilities: Incompatible pairs cannot be on the same team ---
:- assigned(P1, T), assigned(P2, T), incompatible(P1, P2).

% --- Synergy Calculation ---
% For each team, count the number of synergy pairs present in its members' skills.

% Helper: List all skills for a person
person_skills(P, S1; P, S2) :- skill(P, S1), skill(P, S2), S1 < S2.

% Synergy pairs present in a team
synergy_present(T, S1, S2) :-
    assigned(P, T),
    person_skills(P, S1, S2),
    synergy_pair(S1, S2).

% Count synergy pairs per team
synergy_count(T, N) :-
    team(T),
    N = #count { S1, S2 : synergy_present(T, S1, S2) }.

% --- Total Synergy ---
total_synergy(Total) :-
    Total = #sum { N, T : synergy_count(T, N) }.

% --- Optimization: Maximize total synergy ---
#maximize { Total : total_synergy(Total) }.

% --- Show the solution ---
#show assigned/2.
#show leader/2.
#show project_assignment/2.
#show synergy_count/2.
#show total_synergy/1.