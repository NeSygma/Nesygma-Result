%% Instance Data
team(a; b; c; d; e).

%% Match Results: beat(X,Y) means X beat Y
beat(a,b).
beat(b,c).
beat(c,a).
beat(a,d).
beat(d,e).
beat(e,c).
beat(b,e).
beat(d,c).
beat(a,e).
beat(b,d).

%% Domain for positions 1..5
position(1..5).

%% Each team gets exactly one position
1 { ranking(P, T) : position(P) } 1 :- team(T).

%% Each position gets exactly one team
1 { ranking(P, T) : team(T) } 1 :- position(P).

%% Count violations: beat(X,Y) where Y is ranked higher (lower position number) than X
violation(X,Y) :- beat(X,Y), ranking(PX, X), ranking(PY, Y), PX > PY.

%% Total violations
total_violations(N) :- N = #count { X,Y : violation(X,Y) }.

%% Minimize violations
#minimize { 1,X,Y : violation(X,Y) }.

%% Show results
#show ranking/2.
#show total_violations/1.