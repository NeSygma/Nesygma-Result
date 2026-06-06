% Team Formation Problem

% Domain declarations
person(alice). person(bob). person(carol). person(dave).
person(eve). person(frank). person(grace). person(henry).

skill(programming). skill(design). skill(testing). skill(management).
skill(documentation).  % Optional skill

team(team1). team(team2).

% Skills per person
has_skill(alice, programming). has_skill(alice, design).
has_skill(bob, programming). has_skill(bob, testing).
has_skill(carol, design). has_skill(carol, management).
has_skill(dave, testing). has_skill(dave, management).
has_skill(eve, programming). has_skill(eve, documentation).
has_skill(frank, design). has_skill(frank, documentation).
has_skill(grace, testing). has_skill(grace, documentation).
has_skill(henry, management). has_skill(henry, documentation).

% Assignment: each person to exactly one team
1 { member(P, T) : team(T) } 1 :- person(P).

% Each team must have exactly 4 people
4 { member(P, team1) : person(P) } 4.
4 { member(P, team2) : person(P) } 4.

% Each team must cover all required skills
required_skill(S) :- skill(S), S != documentation.

covers(T, S) :- member(P, T), has_skill(P, S), required_skill(S).

% Constraint: each team must cover all required skills
:- team(T), required_skill(S), not covers(T, S).

% Calculate overlap score (to minimize)
% Overlap = number of pairs of people in same team who share a skill
overlap_score(N) :-
    N = #sum { 1, T, P1, P2 : 
        team(T), person(P1), person(P2), P1 < P2,
        member(P1, T), member(P2, T),
        has_skill(P1, S), has_skill(P2, S)
    }.

% Minimize overlap
#minimize { N : overlap_score(N) }.

% Show the solution
#show member/2.
#show team/1.
#show person/1.
#show required_skill/1.
#show covers/2.
#show overlap_score/1.