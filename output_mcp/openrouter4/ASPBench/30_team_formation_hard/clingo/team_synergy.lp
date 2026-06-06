% --- Domain Facts ---
% Teams
team(1;2;3).

% Projects
project(alpha; beta; gamma).

% Personnel
person(alex; ben; chloe; david; grace; harry; eva; frank; ivy; jack; kate; leo).

% Senior/Junior levels
senior(alex; ben; chloe; david; grace; harry).
junior(eva; frank; ivy; jack; kate; leo).

% Skills
skill("Programming"; "Security"; "DevOps"; "Design"; "Management"; "Testing"; "DataScience"; "Cloud").

% Primary skills (used for leader exclusivity)
primary_skill("Programming"; "Design"; "Testing"; "Management"; "DataScience"; "DevOps").

% Person skills
person_skill(alex, "Programming").
person_skill(alex, "Security").
person_skill(ben, "Programming").
person_skill(ben, "DevOps").
person_skill(chloe, "Design").
person_skill(chloe, "Management").
person_skill(david, "Testing").
person_skill(david, "DataScience").
person_skill(grace, "Management").
person_skill(grace, "DataScience").
person_skill(harry, "DevOps").
person_skill(harry, "Security").
person_skill(eva, "Programming").
person_skill(eva, "Cloud").
person_skill(frank, "Design").
person_skill(frank, "Testing").
person_skill(ivy, "Design").
person_skill(ivy, "Cloud").
person_skill(jack, "Testing").
person_skill(jack, "Programming").
person_skill(kate, "Management").
person_skill(kate, "DevOps").
person_skill(leo, "DataScience").
person_skill(leo, "Security").

% Project requirements
project_requires(alpha, "Security").
project_requires(beta, "Cloud").

% Synergy pairs
synergy_pair("Programming", "DevOps").
synergy_pair("Design", "DataScience").
synergy_pair("Management", "Testing").
synergy_pair("Security", "Cloud").

% Incompatibilities
incompatible(alex, ben).
incompatible(chloe, grace).
incompatible(david, harry).

% --- Assignment ---
% Each person to exactly one team
1 { assign(P, T) : team(T) } 1 :- person(P).

% Each team to exactly one project (bijection)
1 { tproj(T, Pr) : project(Pr) } 1 :- team(T).
1 { tproj(T, Pr) : team(T) } 1 :- project(Pr).

% --- Constraints ---
% Each team must have exactly 4 members
:- team(T), #count{P : assign(P, T)} != 4.

% Leadership: exactly one Senior leader per team
1 { leader(T, P) : assign(P, T), senior(P) } 1 :- team(T).

% Leaders must have mutually exclusive primary skills
:- leader(T1, P1), leader(T2, P2), T1 != T2,
   person_skill(P1, S), person_skill(P2, S), primary_skill(S).

% Incompatibilities: specified pairs cannot be on same team
:- assign(P1, T), assign(P2, T), incompatible(P1, P2).

% Project requirements: team assigned to Alpha must have Security
team_has_skill(T, S) :- assign(P, T), person_skill(P, S).
:- tproj(T, alpha), not team_has_skill(T, "Security").
:- tproj(T, beta), not team_has_skill(T, "Cloud").

% --- Synergy Scoring ---
team_synergy_point(T, S1, S2) :- 
    team(T), synergy_pair(S1, S2), 
    team_has_skill(T, S1), team_has_skill(T, S2).

team_synergy_count(T, N) :- 
    team(T),
    N = #count{S1, S2 : team_synergy_point(T, S1, S2)}.

total_synergy(N) :- 
    N = #sum{T, C : team_synergy_count(T, C)}.

% Maximize total synergy
#maximize { 1, T, S1, S2 : team_synergy_point(T, S1, S2) }.

% --- Output ---
#show assign/2.
#show tproj/2.
#show leader/2.
#show team_synergy_count/2.
#show total_synergy/1.