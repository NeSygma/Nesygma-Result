% === Domain ===
team(a). team(b). team(c). team(d). team(e).
pos(1). pos(2). pos(3). pos(4). pos(5).

% === Match Results (X beat Y) ===
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

% === Decision Variables ===
% Each team is assigned exactly one position
1 { rank(T, P) : pos(P) } 1 :- team(T).

% Each position is assigned exactly one team
1 { rank(T, P) : team(T) } 1 :- pos(P).

% === Violation Definition ===
% A violation occurs when X beat Y, but X is ranked LOWER than Y
% (higher position number = lower rank)
violation(X, Y) :- beat(X, Y), rank(X, Px), rank(Y, Py), Px > Py.

% === Count violations ===
violations(N) :- N = #count { X, Y : violation(X, Y) }.

% === Optimization: minimize total violations ===
#minimize { 1, X, Y : violation(X, Y) }.

% === Output ===
#show rank/2.
#show violations/1.