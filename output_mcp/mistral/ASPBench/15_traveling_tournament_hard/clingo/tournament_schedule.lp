%% Basic facts and domains

% Teams
team(a;b;c;d;e;f).

% Rounds (1-10)
round(1..10).

% Initial locations (at round 0, before any games)
initial_location(a, 0, 0).
initial_location(b, 10, 0).
initial_location(c, 5, 8).
initial_location(d, 0, 15).
initial_location(e, 10, 15).
initial_location(f, 15, 8).

% Distance matrix (scaled by 10)
distance(a, b, 100). distance(a, c, 94). distance(a, d, 150).
distance(a, e, 180). distance(a, f, 170).
distance(b, a, 100). distance(b, c, 94). distance(b, d, 180).
distance(b, e, 150). distance(b, f, 94).
distance(c, a, 94). distance(c, b, 94). distance(c, d, 86).
distance(c, e, 86). distance(c, f, 100).
distance(d, a, 150). distance(d, b, 180). distance(d, c, 86).
distance(d, e, 100). distance(d, f, 170).
distance(e, a, 180). distance(e, b, 150). distance(e, c, 86).
distance(e, d, 100). distance(e, f, 94).
distance(f, a, 170). distance(f, b, 94). distance(f, c, 100).
distance(f, d, 170). distance(f, e, 94).

% Helper: all ordered pairs of distinct teams
ordered_pair(T1, T2) :- team(T1), team(T2), T1 != T2.

%% Schedule generation
% Choose matches for each round (3 matches per round)
1 { match(R, H, A) : team(H), team(A), H != A } 3 :- round(R).

% Each ordered pair plays exactly once
:- ordered_pair(T1, T2), not match(R, T1, T2), not match(R, T2, T1), round(R).

% Each team plays exactly once per round
:- team(T), round(R), #count{ M : match(R, H, A), (H=T ; A=T) } != 1.

% Rivalry constraint: A vs B and C vs D cannot play in round 1
:- match(1, a, b).
:- match(1, b, a).
:- match(1, c, d).
:- match(1, d, c).

%% Stateful travel and location tracking

% Team home coordinates
team_coords(T, X, Y) :- initial_location(T, X, Y).

% Location at round 0 (initial)
location(T, 0, X, Y) :- initial_location(T, X, Y).

% Location after round R is determined by the match in round R
% If team plays home: location = home coordinates
% If team plays away: location = away coordinates

% Base case for consecutive counts
consecutive_home(T, 0, 0) :- team(T).
consecutive_away(T, 0, 0) :- team(T).

% Update location and consecutive counts for each round
location(T, R, X, Y) :- 
    match(R, T, _),  % Team T plays home
    team_coords(T, X, Y),
    round(R),
    R > 0.

location(T, R, X, Y) :- 
    match(R, _, T),  % Team T plays away at opponent's venue
    team_coords(T, X, Y),
    round(R),
    R > 0.

% Update consecutive home count
consecutive_home(T, R, C+1) :- 
    consecutive_home(T, R-1, C),
    match(R, T, _),
    C < 3,
    round(R),
    R > 0.

% Update consecutive away count
consecutive_away(T, R, C+1) :- 
    consecutive_away(T, R-1, C),
    match(R, _, T),
    C < 3,
    round(R),
    R > 0.

% Reset consecutive counts when switching between home/away
consecutive_home(T, R, 1) :- 
    match(R, T, _),
    match(R-1, _, T),
    round(R),
    R > 0.

consecutive_away(T, R, 1) :- 
    match(R, _, T),
    match(R-1, T, _),
    round(R),
    R > 0.

% Constraint: no more than 3 consecutive home or away games
:- consecutive_home(T, R, C), C > 3, team(T), round(R).
:- consecutive_away(T, R, C), C > 3, team(T), round(R).

%% Mandatory home stand
% Each team must have at least one sequence of 2 consecutive home games
has_home_stand(T) :- match(R, T, _), match(R+1, T, _), team(T), round(R), R < 10.
:- team(T), not has_home_stand(T).

%% Travel fatigue constraint

% Calculate travel distance for away games
% Distance is from team's location at end of previous round to away venue

travel_distance(R, T, D) :- 
    match(R, _, A),  % T plays away at A in round R
    team(T),
    team(A),
    T != A,
    location(T, R-1, X1, Y1),  % T's location at end of R-1
    team_coords(A, X2, Y2),     % A's home coordinates
    distance(T, A, D),          % Precomputed distance
    D > 140,
    round(R),
    R > 0.

% If travel distance > 140, next game must be home (if round exists)
:- travel_distance(R, T, D), match(R+1, _, T), round(R), R < 10.

%% Show the schedule
#show match/3.