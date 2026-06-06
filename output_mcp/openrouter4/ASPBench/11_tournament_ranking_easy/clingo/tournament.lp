%% Tournament Ranking Problem
%% Find optimal ranking that minimizes violations

%% Domain
team(a; b; c; d; e).
position(1..5).

%% Match results (X beat Y)
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

%% 1. Choice: assign each position exactly one team
1 { ranking(P, T) : team(T) } 1 :- position(P).

%% 2. Each team must appear exactly once in the ranking
1 { ranking(P, T) : position(P) } 1 :- team(T).

%% 3. Count violations: when lower-ranked (higher P) beat higher-ranked (lower P)
violation(X, Y) :- beat(X, Y), ranking(PX, X), ranking(PY, Y), PX > PY.

%% Count total violations
total_violations(N) :- N = #count { X, Y : violation(X, Y) }.

%% Minimize violations
#minimize { 1, X, Y : violation(X, Y) }.

%% Show results
#show ranking/2.
#show total_violations/1.