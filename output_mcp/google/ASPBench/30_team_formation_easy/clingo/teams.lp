% --- Data ---
person(alice; bob; carol; dave; eve; frank; grace; henry).
team(1; 2).
required(programming; design; testing; management).

has_skill(alice, programming). has_skill(alice, design).
has_skill(bob, programming). has_skill(bob, testing).
has_skill(carol, design). has_skill(carol, management).
has_skill(dave, testing). has_skill(dave, management).
has_skill(eve, programming). has_skill(eve, documentation).
has_skill(frank, design). has_skill(frank, documentation).
has_skill(grace, testing). has_skill(grace, documentation).
has_skill(henry, management). has_skill(henry, documentation).

% --- Logic ---
% Each person assigned to exactly one team
{ assigned(P, T) : team(T) } = 1 :- person(P).

% Each team must have exactly 4 people
:- team(T), #count { P : assigned(P, T) } != 4.

% Each team must have at least one person with each required skill
team_has_skill(T, S) :- team(T), required(S), assigned(P, T), has_skill(P, S).
:- team(T), required(S), not team_has_skill(T, S).

% Minimize skill overlap
% Count how many people in team T have skill S
count_skill(T, S, C) :- team(T), required(S), C = #count { P : assigned(P, T), has_skill(P, S) }.

% Overlap is (count - 1) if count > 1, else 0
overlap(T, S, N) :- count_skill(T, S, C), N = C - 1, N > 0.

#minimize { N, T, S : overlap(T, S, N) }.

#show assigned/2.