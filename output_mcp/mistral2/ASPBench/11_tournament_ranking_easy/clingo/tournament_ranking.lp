% Declare the teams
team(a). team(b). team(c). team(d). team(e).

% Match results (X beat Y)
beat(a, b). beat(b, c). beat(c, a). beat(a, d). beat(d, e).
beat(e, c). beat(b, e). beat(d, c). beat(a, e). beat(b, d).

% Generate all possible rankings (each team gets a unique rank from 1 to 5)
{ rank(T, R) : R = 1..5 } = 1 :- team(T).

% Ensure each rank is assigned to exactly one team
:- rank(T1, R), rank(T2, R), T1 != T2.

% Count violations: For each beat(X, Y), if Y is ranked higher than X, count a violation
violation :- beat(X, Y), rank(Y, R1), rank(X, R2), R1 < R2.

% Count the total number of violations
total_violations(N) :- N = #count{ V : violation, V = 1 }.

% Minimize the number of violations
#minimize{ N : total_violations(N) }.

% Show the ranking and total violations
#show rank/2.
#show total_violations/1.