% Teams and Rounds
team(a; b; c; d).
round(1..6).

% Distance Matrix (multiplied by 10 to handle decimals as integers)
dist(a, b, 50). dist(b, a, 50).
dist(a, c, 60). dist(c, a, 60).
dist(a, d, 82). dist(d, a, 82).
dist(b, c, 50). dist(c, b, 50).
dist(b, d, 57). dist(d, b, 57).
dist(c, d, 100). dist(d, c, 100).

% Each round has exactly 2 matches (4 teams, each plays once)
% play(Home, Away, Round)
{ play(H, A, R) : team(H), team(A), H != A } = 2 :- round(R).

% Each team plays exactly once per round
:- round(R), team(T), not 1 { play(T, _, R) ; play(_, T, R) } 1.

% Double round-robin: Each pair plays exactly twice (once home, once away)
:- team(T1), team(T2), T1 != T2, not 1 { play(T1, T2, R) : round(R) } 1.
:- team(T1), team(T2), T1 != T2, not 1 { play(T2, T1, R) : round(R) } 1.

% Consecutive limit: No team plays more than 2 consecutive home games
% A team plays home if it is the first argument in play(H, A, R)
is_home(T, R) :- play(T, _, R).
:- team(T), round(R), R <= 4, is_home(T, R), is_home(T, R+1), is_home(T, R+2).

% Consecutive limit: No team plays more than 2 consecutive away games
% A team plays away if it is the second argument in play(H, A, R)
is_away(T, R) :- play(_, T, R).
:- team(T), round(R), R <= 4, is_away(T, R), is_away(T, R+1), is_away(T, R+2).

% Objective: Minimize total travel distance
% Distance is only for the away team
total_distance(D) :- D = #sum { Dist, H, A, R : play(H, A, R), dist(A, H, Dist) }.
#minimize { D : total_distance(D) }.

% Output
#show play/3.
#show total_distance/1.