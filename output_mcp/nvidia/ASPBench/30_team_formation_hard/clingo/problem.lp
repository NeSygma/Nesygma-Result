person(alex). person(bob). person(chloe). person(david). person(grace). person(harry). person(eva). person(frank). person(ivy). person(jack). person(kate). person(leo).
senior(alex). senior(bob). senior(chloe). senior(david). senior(grace). senior(harry).
skill(alex, programming). skill(alex, security).
skill(bob, programming). skill(bob, devops).
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
incompatible(alex, ben).
incompatible(chloe, grace).
incompatible(david, harry).
project(alpha). project(beta). project(gamma).
team(1). team(2). team(3).

4 { assignment(T, P) : person(P) } 4 :- team(T).
1 { assignment(T, P) : team(T) } 1 :- person(P).

{ leader(T, L) : senior(L), assignment(T, L) }.
1 { leader(T, L) : senior(L), assignment(T, L) } :- team(T).
:- leader(T1, L), leader(T2, L), T1 != T2.

{ team_project(T, P) : project(P) }.
1 { team_project(T, P) : project(P) } :- team(T).
1 { team_project(T1, P), team_project(T2, P), T1 != T2 } :- project(P).

:- team_project(T, alpha), not team_has_skill(T, security).
:- team_project(T, beta), not team_has_skill(T, cloud).

team_has_skill(T, Skill) :- assignment(T, P), skill(P, Skill).

:- incompatible(P1, P2), assignment(T, P1), assignment(T, P2).

pair_earned(T, prog_dev) :- team_has_skill(T, programming), team_has_skill(T, devops).
pair_earned(T, design_datasci) :- team_has_skill(T, design), team_has_skill(T, datasci).
pair_earned(T, management_testing) :- team_has_skill(T, management), team_has_skill(T, testing).
pair_earned(T, security_cloud) :- team_has_skill(T, security), team_has_skill(T, cloud).

earned(T, prog_dev) :- pair_earned(T, prog_dev).
earned(T, design_datasci) :- pair_earned(T, design_datasci).
earned(T, management_testing) :- pair_earned(T, management_testing).
earned(T, security_cloud) :- pair_earned(T, security_cloud).

team_synergy(T, S) :- team(T), S = #count { P : earned(T,P) }.

total_synergy(N) :- N = #count { E : earned(E) }.
#maximize { N : total_synergy(N) }.
#show total_synergy/1.

team_fact(T, P, L, M1, M2, M3, M4, S) :-
    team(T), assignment(T, M1), assignment(T, M2), assignment(T, M3), assignment(T, M4), different(M1, M2, M3, M4), leader(T, L), team_project(T, P), team_synergy(T, S).

#show team_fact/8.
#show total_synergy/1.