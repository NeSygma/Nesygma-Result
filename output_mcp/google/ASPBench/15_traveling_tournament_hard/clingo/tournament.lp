% Teams and Locations
team(a; b; c; d; e; f).
round(1..10).

% Distance matrix (scaled by 10)
dist(a, b, 100). dist(a, c, 94). dist(a, d, 150). dist(a, e, 180). dist(a, f, 170).
dist(b, c, 94). dist(b, d, 180). dist(b, e, 150). dist(b, f, 94).
dist(c, d, 86). dist(c, e, 86). dist(c, f, 100).
dist(d, e, 100). dist(d, f, 170).
dist(e, f, 94).
dist(X, Y, D) :- dist(Y, X, D).
dist(X, X, 0) :- team(X).

% 1. Double Round-Robin
{ match(H, A, R) : round(R) } = 1 :- team(H), team(A), H != A.

% 2. Round Structure
plays(T, R) :- match(T, _, R).
plays(T, R) :- match(_, T, R).
:- round(R), team(T), not plays(T, R).
:- round(R), #count { H, A : match(H, A, R) } != 3.

% 3. Stateful Travel
is_home(T, R) :- match(T, _, R).
is_away(T, R) :- match(_, T, R).

% location(T, R, L) means team T is at the home city of team L at the end of round R.
location(T, R, T) :- is_home(T, R).
location(T, R, H) :- is_away(T, R), match(H, T, R).
location(T, 0, T) :- team(T).

% 4. Consecutive Game Limit
:- team(T), round(R), R <= 8, is_home(T, R), is_home(T, R+1), is_home(T, R+2), is_home(T, R+3).
:- team(T), round(R), R <= 8, is_away(T, R), is_away(T, R+1), is_away(T, R+2), is_away(T, R+3).

% 5. Rivalry Constraint
:- match(a, b, 1). :- match(b, a, 1).
:- match(c, d, 1). :- match(d, c, 1).

% 6. Mandatory Break
has_home_stand(T) :- team(T), round(R), R < 10, is_home(T, R), is_home(T, R+1).
:- team(T), not has_home_stand(T).

% 7. Travel Fatigue
:- team(T), round(R), R < 10, is_away(T, R), match(H, T, R),
   location(T, R-1, L_prev), dist(L_prev, H, D), D > 140, not is_home(T, R+1).

% Final Answer Mapping
option(feasible) :- match(_, _, _).
#show option/1.