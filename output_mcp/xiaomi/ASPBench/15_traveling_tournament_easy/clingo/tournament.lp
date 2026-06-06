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
% A match is (home, away) where home hosts away
{ match(R, H, A) : team(H), team(A), H != A } 2 :- round(R).

% Each team plays exactly once per round
1 { match(R, H, A) : team(A), H != A } 1 :- round(R), team(H).
1 { match(R, H, A) : team(H), H != A } 1 :- round(R), team(A).

% Derive play status
plays(R, T) :- match(R, T, _).  % home team plays
plays(R, T) :- match(R, _, T).  % away team plays

home(R, T) :- match(R, T, _).
away(R, T) :- match(R, _, T).

% Each team plays exactly once per round (enforced)
:- round(R), team(T), not plays(R, T).

% Double round-robin: each pair plays exactly twice (once home each)
% For each pair (T1, T2), exactly one match where T1 hosts T2
1 { match(R, T1, T2) : round(R) } 1 :- pair(T1, T2).
% For each pair (T1, T2), exactly one match where T2 hosts T1
1 { match(R, T2, T1) : round(R) } 1 :- pair(T1, T2).

% Consecutive home games: no more than 2 in a row
% Track consecutive home games
consecutive_home(T, R, 1) :- home(R, T), round(R), not home(R-1, T).
consecutive_home(T, R, N+1) :- home(R, T), round(R), R > 1, consecutive_home(T, R-1, N), N < 3.

% Forbid 3+ consecutive home games
:- consecutive_home(T, R, 3).

% Consecutive away games: no more than 2 in a row
consecutive_away(T, R, 1) :- away(R, T), round(R), not away(R-1, T).
consecutive_away(T, R, N+1) :- away(R, T), round(R), R > 1, consecutive_away(T, R-1, N), N < 3.

% Forbid 3+ consecutive away games
:- consecutive_away(T, R, 3).

% Travel distance: away team travels to home team's city
travel(R, A, D) :- match(R, H, A), dist(A, H, D).

% Total travel distance
total_distance(D) :- D = #sum { Dist, R, A : travel(R, A, Dist) }.

% Minimize total travel distance
#minimize { D : total_distance(D) }.

% Output
#show match/3.
#show total_distance/1.