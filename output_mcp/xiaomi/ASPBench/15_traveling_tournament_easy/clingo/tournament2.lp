% Domain: Teams
team(a). team(b). team(c). team(d).

% Domain: Rounds (1..6)
round(1). round(2). round(3). round(4). round(5). round(6).

% Distance matrix (Euclidean distances)
dist(a, b, 5). dist(a, c, 6). dist(a, d, 8).
dist(b, a, 5). dist(b, c, 5). dist(b, d, 6).
dist(c, a, 6). dist(c, b, 5). dist(c, d, 10).
dist(d, a, 8). dist(d, b, 6). dist(d, c, 10).

% All ordered pairs of distinct teams
pair(T1, T2) :- team(T1), team(T2), T1 < T2.

% Generate matches: each round has exactly 2 matches
{ match(R, H, A) : team(H), team(A), H != A } 2 :- round(R).

% Each team plays exactly once per round (as home or away)
plays(R, T) :- match(R, T, _).  % home team plays
plays(R, T) :- match(R, _, T).  % away team plays

home(R, T) :- match(R, T, _).
away(R, T) :- match(R, _, T).

% Each team plays exactly once per round
:- round(R), team(T), not plays(R, T).

% Double round-robin: each pair plays exactly twice (once home each)
1 { match(R, T1, T2) : round(R) } 1 :- pair(T1, T2).
1 { match(R, T2, T1) : round(R) } 1 :- pair(T1, T2).

% Consecutive home games: no more than 2 in a row
% Use helper to track consecutive home games
prev_home(T, R) :- home(R, T), round(R), R > 1, home(R-1, T).

% Forbid 3 consecutive home games
:- round(R), R > 2, home(R, T), home(R-1, T), home(R-2, T).

% Forbid 3 consecutive away games
:- round(R), R > 2, away(R, T), away(R-1, T), away(R-2, T).

% Travel distance: away team travels to home team's city
travel(R, A, D) :- match(R, H, A), dist(A, H, D).

% Total travel distance
total_distance(D) :- D = #sum { Dist, R, A : travel(R, A, Dist) }.

% Minimize total travel distance
#minimize { D : total_distance(D) }.

% Output
#show match/3.
#show total_distance/1.