% ===== DOMAIN FACTS =====
person(alice). person(bob). person(carol). person(dave).
person(eve). person(frank). person(grace). person(henry).

team(1). team(2).

% Skills
skill(programming). skill(design). skill(testing). skill(management). skill(documentation).

% Required skills (must be covered by each team)
required_skill(programming).
required_skill(design).
required_skill(testing).
required_skill(management).

% ===== SKILL DATA =====
has_skill(alice, programming). has_skill(alice, design).
has_skill(bob, programming). has_skill(bob, testing).
has_skill(carol, design). has_skill(carol, management).
has_skill(dave, testing). has_skill(dave, management).
has_skill(eve, programming). has_skill(eve, documentation).
has_skill(frank, design). has_skill(frank, documentation).
has_skill(grace, testing). has_skill(grace, documentation).
has_skill(henry, management). has_skill(henry, documentation).

% ===== ASSIGNMENT =====
% Each person assigned to exactly one team
1 { assigned(P, T) : team(T) } 1 :- person(P).

% Each team has exactly 4 people
4 { assigned(P, T) : person(P) } 4 :- team(T).

% ===== SKILL COVERAGE =====
% A team has a skill if at least one member has it
team_has_skill(T, S) :- team(T), skill(S), assigned(P, T), has_skill(P, S).

% Each team must have all required skills
:- team(T), required_skill(S), not team_has_skill(T, S).

% ===== SKILL OVERLAP (for minimization) =====
% Count how many people in each team have each skill
skill_count(T, S, N) :- team(T), skill(S), 
    N = #count { P : assigned(P, T), has_skill(P, S) }.

% Overlap is the excess beyond 1 person per skill per team
% We want to minimize total overlap across all teams and skills
overlap(T, S, O) :- skill_count(T, S, N), O = N - 1, N > 1.
overlap(T, S, 0) :- skill_count(T, S, N), N <= 1.

total_overlap(N) :- N = #sum { O, T, S : overlap(T, S, O) }.

% Minimize total skill overlap
#minimize { O, T, S : overlap(T, S, O) }.

% ===== OUTPUT =====
#show assigned/2.
#show team_has_skill/2.
#show total_overlap/1.