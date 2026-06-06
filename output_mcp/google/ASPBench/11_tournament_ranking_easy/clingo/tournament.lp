% Teams
team(a; b; c; d; e).

% Match Results (beat(Winner, Loser))
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

% Each team has exactly one rank (1 to 5)
1 { rank(T, P) : P = 1..5 } 1 :- team(T).
1 { rank(T, P) : team(T) } 1 :- P = 1..5.

% A violation occurs when a match beat(X,Y) occurs where Y is ranked higher than X
% (Higher rank means a smaller position number, e.g., 1st place is rank 1)
violation(W, L) :- beat(W, L), rank(W, Rw), rank(L, Rl), Rl < Rw.

% Objective: Minimize total violations
#minimize { 1, W, L : violation(W, L) }.

% Output
#show rank/2.
#show violation/2.
#show total_violations/1.
total_violations(N) :- N = #count { W, L : violation(W, L) }.