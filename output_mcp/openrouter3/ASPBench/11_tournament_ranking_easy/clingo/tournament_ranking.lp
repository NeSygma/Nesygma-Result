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

% Ranking: position(Team, Rank) where Rank 1 is best, Rank 5 is worst
% Each team gets exactly one position
1 { position(T, R) : team(T) } 1 :- rank(R).
rank(1..5).

% Each rank gets exactly one team
1 { position(T, R) : rank(R) } 1 :- team(T).

% Violation: beat(X, Y) but Y is ranked higher than X (position(Y) < position(X))
violation(X, Y) :- beat(X, Y), position(X, PosX), position(Y, PosY), PosY < PosX.

% Count total violations
total_violations(N) :- N = #count { X, Y : violation(X, Y) }.

% Minimize violations
#minimize { N : total_violations(N) }.

% Show the solution
#show position/2.
#show total_violations/1.
#show beat/2.