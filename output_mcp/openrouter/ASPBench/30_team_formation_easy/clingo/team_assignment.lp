% Persons
person(alice). person(bob). person(carol). person(dave). person(eve). person(frank). person(grace). person(henry).

% Required skills
skill(programming). skill(design). skill(testing). skill(management).

% Person skills (only required ones)
person_skill(alice, programming). person_skill(alice, design).
person_skill(bob, programming). person_skill(bob, testing).
person_skill(carol, design). person_skill(carol, management).
person_skill(dave, testing). person_skill(dave, management).
person_skill(eve, programming).
person_skill(frank, design).
person_skill(grace, testing).
person_skill(henry, management).

% Teams
team(1..2).

% Each person assigned to exactly one team (symmetry break: alice to team 1)
assigned(alice,1).
1 { assigned(P,1); assigned(P,2) } 1 :- person(P), P != alice.

% Team size exactly 4
:- team(T), #count{ P : assigned(P,T) } != 4.

% Skill coverage: each team must have at least one person with each required skill
has_skill(T,S) :- assigned(P,T), person_skill(P,S).
:- team(T), skill(S), not has_skill(T,S).

% Count skill occurrences per team (make variables safe)
skill_count(T,S,C) :- team(T), skill(S), C = #count{ P : assigned(P,T), person_skill(P,S) }.

% Overlap minimization: minimize extra persons per skill per team
#minimize { (C-1)@1, T, S : skill_count(T,S,C), C > 1 }.

#show assigned/2.