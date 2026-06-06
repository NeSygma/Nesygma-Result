% ============ Domain ============
person(alice). person(bob). person(carol). person(dave).
person(eve). person(frank). person(grace). person(henry).

team(team1). team(team2).

skill(programming). skill(design). skill(testing). skill(management). skill(documentation).
required_skill(programming). required_skill(design). required_skill(testing). required_skill(management).

% ============ Skills per person ============
has_skill(alice, programming). has_skill(alice, design).
has_skill(bob, programming). has_skill(bob, testing).
has_skill(carol, design). has_skill(carol, management).
has_skill(dave, testing). has_skill(dave, management).
has_skill(eve, programming). has_skill(eve, documentation).
has_skill(frank, design). has_skill(frank, documentation).
has_skill(grace, testing). has_skill(grace, documentation).
has_skill(henry, management). has_skill(henry, documentation).

% ============ Assignment: each person to exactly one team ============
1 { assigned(P, T) : team(T) } 1 :- person(P).

% ============ Each team has exactly 4 people ============
4 { assigned(P, T) : person(P) } 4 :- team(T).

% ============ Derived: team has a skill if at least one member has it ============
team_has_skill(T, S) :- assigned(P, T), has_skill(P, S), team(T), skill(S).

% ============ Constraint: each team must cover all required skills ============
:- team(T), required_skill(S), not team_has_skill(T, S).

% ============ Overlap detection: skill S overlaps in team T if >=2 members share it ============
overlap(T, S) :- assigned(P1, T), assigned(P2, T), P1 < P2,
                 has_skill(P1, S), has_skill(P2, S), team(T), skill(S).

% ============ Objective: minimize skill overlap within teams ============
#minimize { 1, T, S : overlap(T, S) }.

% ============ Output ============
#show assigned/2.
#show team_has_skill/2.
#show overlap/2.