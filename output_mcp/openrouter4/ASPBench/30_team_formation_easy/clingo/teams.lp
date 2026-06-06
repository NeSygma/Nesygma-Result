% Define people
person(alice; bob; carol; dave; eve; frank; grace; henry).

% Define all skills
skill("Programming"; "Design"; "Testing"; "Management"; "Documentation").

% Required skills for team formation
req_skill("Programming"; "Design"; "Testing"; "Management").

% Person skills (each person has exactly 2 skills)
person_skill(alice, "Programming").
person_skill(alice, "Design").
person_skill(bob, "Programming").
person_skill(bob, "Testing").
person_skill(carol, "Design").
person_skill(carol, "Management").
person_skill(dave, "Testing").
person_skill(dave, "Management").
person_skill(eve, "Programming").
person_skill(eve, "Documentation").
person_skill(frank, "Design").
person_skill(frank, "Documentation").
person_skill(grace, "Testing").
person_skill(grace, "Documentation").
person_skill(henry, "Management").
person_skill(henry, "Documentation").

% Two teams
team(1..2).

% Constraint 1 & 2: Each person assigned to exactly one team
1 { assigned(P, T) : team(T) } 1 :- person(P).

% Each team has exactly 4 people
:- team(T), #count { P : assigned(P, T) } != 4.

% Constraint 3: Each team must have at least one person with each required skill
has_skill_in_team(T, S) :- assigned(P, T), person_skill(P, S).
:- team(T), req_skill(S), not has_skill_in_team(T, S).

% Constraint 4: Minimize skill overlap within teams
% For each (team, skill), count how many people have that skill
skill_count(T, S, C) :- C = #count { P : assigned(P, T), person_skill(P, S) }, team(T), skill(S).

% For required skills: overlap = C - 1 (since first occurrence is required)
% For non-required skills: overlap = C (since minimum is 0)
overlap_value(T, S, C)     :- skill_count(T, S, C), not req_skill(S).
overlap_value(T, S, C - 1) :- skill_count(T, S, C), req_skill(S), C >= 1.

% Minimize total overlap
#minimize { O, T, S : overlap_value(T, S, O) }.

% Display team composition
member(P, T) :- assigned(P, T).
team_members(T, P) :- assigned(P, T).

% For pretty output - show team members
#show team_members/2.