% Teams
team(a). team(b). team(c). team(d). team(e).

% Match results: beat(X, Y) means X beat Y
beat(a, b).
beat(b, c).
beat(c, a).
beat(a, d).
beat(d, e).
beat(e, c).
beat(b, e).
beat(d, c).
beat(a, e).
beat(b, d).

% Ranking: assign each team a unique rank from 1 to 5 (1 is best, 5 is worst)
1 { rank(T, R) : team(T) } 1 :- rank_domain(R).
rank_domain(1..5).

% Ensure each rank is used exactly once (by the choice rule above, each rank gets exactly one team)
% Actually, the choice rule ensures each team gets exactly one rank, but we also need each rank used exactly once.
% We can add a constraint: each rank must be assigned to exactly one team.
% But the choice rule already ensures each team gets one rank, and there are 5 teams and 5 ranks, so it's a bijection.
% However, to be safe, we can add: 1 { rank(T, R) : team(T) } 1 :- rank_domain(R). This ensures each rank is assigned to exactly one team.
% But note: the choice rule above is per rank? Actually, the rule is: for each rank R, we choose exactly one team T to have that rank.
% That's correct.

% Define violation: beat(X, Y) and rank(X) > rank(Y) (X is lower-ranked than Y)
violation(X, Y) :- beat(X, Y), rank(X, RX), rank(Y, RY), RX > RY.

% Count violations
#show violations/0.
violations(N) :- N = #count { X, Y : violation(X, Y) }.

% Minimize violations
:~ violations(N). [1@1, N]

% Show ranking: list teams in order of rank
#show ranking/0.
ranking :- team(T), rank(T, R), R = 1, write("1st: ", T), nl,
           team(T2), rank(T2, R2), R2 = 2, write("2nd: ", T2), nl,
           team(T3), rank(T3, R3), R3 = 3, write("3rd: ", T3), nl,
           team(T4), rank(T4, R4), R4 = 4, write("4th: ", T4), nl,
           team(T5), rank(T5, R5), R5 = 5, write("5th: ", T5), nl.

% Alternatively, show each team's rank
#show rank/2.
#show violations/1.