% --- DOMAINS ---
team(a; b; c; d).
round(0..5).
match(0; 1).

% --- LOCATIONS ---
location(a, 0, 0).
location(b, 3, 4).
location(c, 6, 0).
location(d, 2, 8).

% --- DISTANCE MATRIX ---
distance(a, b, 5).
distance(a, c, 6).
distance(a, d, 8.2).
distance(b, a, 5).
distance(b, c, 5).
distance(b, d, 5.7).
distance(c, a, 6).
distance(c, b, 5).
distance(c, d, 10).
distance(d, a, 8.2).
distance(d, b, 5.7).
distance(d, c, 10).

% --- HELPER PREDICATE: Squared Euclidean distance (for grounding) ---
sq_dist(T1, T2, D) :-
    location(T1, X1, Y1),
    location(T2, X2, Y2),
    D = (X1 - X2) * (X1 - X2) + (Y1 - Y2) * (Y1 - Y2).

% --- MATCH SCHEDULE ---
% Each round has exactly 2 matches
{ plays(R, M, T1, T2) : team(T1), team(T2), T1 != T2 } = 2 :- round(R), match(M).

% Each team plays exactly once per round
:- round(R), team(T), #count{ T2 : plays(R, _, T, T2) } != 1.
:- round(R), team(T), #count{ T1 : plays(R, _, T1, T) } != 1.

% Double round-robin: each pair plays exactly twice (home/away swapped)
:- team(T1), team(T2), T1 < T2,
   #count{ R, M : plays(R, M, T1, T2) } != 1.
:- team(T1), team(T2), T1 < T2,
   #count{ R, M : plays(R, M, T2, T1) } != 1.

% --- HOME/AWAY ASSIGNMENT ---
home(M, T) :- plays(_, M, T, _).
away(M, T) :- plays(_, M, _, T).

% --- TRAVEL DISTANCE ---
% For each round and team, compute travel distance
% Use squared distance for grounding, but we will sum actual distances in minimization
% Since we cannot compute sqrt in minimization, we will use squared distance as a proxy
% Alternatively, we can precompute the distances and use them directly

travel_distance(R, T, D) :-
    round(R),
    team(T),
    plays(R, M, T, T2),
    distance(T, T2, D).

% --- CONSECUTIVE HOME/AWAY LIMITS ---
% Base case: 1 consecutive home/away game
consecutive_home(R, T, 1) :-
    round(R),
    team(T),
    plays(R, _, T, _),
    not prev_plays_home(R, T).

consecutive_away(R, T, 1) :-
    round(R),
    team(T),
    plays(R, _, _, T),
    not prev_plays_away(R, T).

prev_plays_home(R, T) :-
    round(R),
    team(T),
    R > 0,
    plays(R-1, _, T, _).

prev_plays_away(R, T) :-
    round(R),
    team(T),
    R > 0,
    plays(R-1, _, _, T).

% Inductive case: extend consecutive home/away games
consecutive_home(R, T, N) :-
    round(R),
    team(T),
    N > 1,
    N = N1 + 1,
    consecutive_home(R-1, T, N1),
    plays(R, _, T, _).

consecutive_away(R, T, N) :-
    round(R),
    team(T),
    N > 1,
    N = N1 + 1,
    consecutive_away(R-1, T, N1),
    plays(R, _, _, T).

% Constraint: no team has >2 consecutive home/away games
:- team(T), round(R), consecutive_home(R, T, N), N > 2.
:- team(T), round(R), consecutive_away(R, T, N), N > 2.

% --- OBJECTIVE: MINIMIZE TOTAL TRAVEL DISTANCE ---
#minimize { D, R, T : travel_distance(R, T, D) }.

% --- SHOW DIRECTIVE ---
#show plays/4.
#show travel_distance/3.