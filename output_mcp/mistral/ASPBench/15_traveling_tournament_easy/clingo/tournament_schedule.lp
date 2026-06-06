% Teams and locations
team(a). team(b). team(c). team(d).

location(a, 0, 0).
location(b, 3, 4).
location(c, 6, 0).
location(d, 2, 8).

% Distance matrix (symmetric) - scaled by 10 to avoid decimals
distance(a, b, 50). distance(b, a, 50).
distance(a, c, 60). distance(c, a, 60).
distance(a, d, 82). distance(d, a, 82).
distance(b, c, 50). distance(c, b, 50).
distance(b, d, 57). distance(d, b, 57).
distance(c, d, 100). distance(d, c, 100).

% Rounds
round(1). round(2). round(3). round(4). round(5). round(6).

% Choice rule: assign matches to rounds
% Each round has exactly 2 matches
{ match(R, H, A) : team(H), team(A), H != A } = 2 :- round(R).

% Each team plays exactly once per round
:- round(R), team(T),
   #count{ H : match(R, H, A), H = T } != 1,
   #count{ A : match(R, H, A), A = T } != 0.
:- round(R), team(T),
   #count{ H : match(R, H, A), H = T } != 0,
   #count{ A : match(R, H, A), A = T } != 1.

% Each pair plays exactly twice (once home, once away)
:- team(H), team(A), H < A, #count{ R : match(R, H, A) } != 1.
:- team(H), team(A), H < A, #count{ R : match(R, A, H) } != 1.

% Track home and away games for consecutive limits
home_game(R, T) :- match(R, T, _).
away_game(R, T) :- match(R, _, T).

% Consecutive home games limit: no team plays 3 consecutive home games
:- team(T), R = 1..4,
   home_game(R, T),
   home_game(R+1, T),
   home_game(R+2, T).

% Consecutive away games limit: no team plays 3 consecutive away games
:- team(T), R = 1..4,
   away_game(R, T),
   away_game(R+1, T),
   away_game(R+2, T).

% Calculate travel distance for each match
% Away team travels from their home to opponent's location
travel_distance(R, A, D) :- match(R, H, A), distance(A, H, D).

% Total distance is the sum of all travel distances
total_distance(D) :- D = #sum{ D1 : travel_distance(_, _, D1) }.

% Minimize total travel distance
#minimize{ D : total_distance(D) }.

% Show the schedule and total distance
#show match/3.
#show total_distance/1.