% Teams
team(a). team(b). team(c). team(d). team(e). team(f).

% Rounds
round(1..10).

% Home locations (team -> city)
home_city(a, (0,0)).
home_city(b, (10,0)).
home_city(c, (5,8)).
home_city(d, (0,15)).
home_city(e, (10,15)).
home_city(f, (15,8)).

% Distance matrix (scaled by 10)
dist(a,b,100). dist(a,c,94). dist(a,d,150). dist(a,e,180). dist(a,f,170).
dist(b,c,94). dist(b,d,180). dist(b,e,150). dist(b,f,94).
dist(c,d,86). dist(c,e,86). dist(c,f,100).
dist(d,e,100). dist(d,f,170).
dist(e,f,94).
% Symmetric distances
dist(b,a,100). dist(c,a,94). dist(d,a,150). dist(e,a,180). dist(f,a,170).
dist(c,b,94). dist(d,b,180). dist(e,b,150). dist(f,b,94).
dist(d,c,86). dist(e,c,86). dist(f,c,100).
dist(e,d,100). dist(f,d,170).
dist(f,e,94).

% Generate matches: each round has exactly 3 matches
{ match(R, H, A) : team(H), team(A), H != A } 3 :- round(R).

% Constraint 1: Double round-robin - each ordered pair plays exactly once
1 { match(R, T1, T2) : round(R) } 1 :- team(T1), team(T2), T1 != T2.

% Constraint 2: Each team plays exactly once per round
% Team appears as home exactly once per round
1 { match(R, T, A) : team(A), T != A } 1 :- round(R), team(T).
% Team appears as away exactly once per round
1 { match(R, H, T) : team(H), H != T } 1 :- round(R), team(T).

% Helper: team plays in round
plays(R, T) :- match(R, T, _).
plays(R, T) :- match(R, _, T).

% Helper: home/away game
home_game(R, T) :- match(R, T, _).
away_game(R, T) :- match(R, _, T).

% Constraint 3: Stateful travel - track location
% Initial location (before round 1) is home city
location(0, T, L) :- home_city(T, L).

% After home game, team is at home city
location(R, T, L) :- match(R, T, _), home_city(T, L), round(R).

% After away game, team is at opponent's home city
location(R, T, L) :- match(R, Opponent, T), home_city(Opponent, L), round(R).

% Constraint 4: No more than 3 consecutive home or away games
% Count consecutive home games
consecutive_home(1, T) :- home_game(1, T).
consecutive_home(R, T) :- home_game(R, T), consecutive_home(R-1, T), R > 1.

% Count consecutive away games
consecutive_away(1, T) :- away_game(1, T).
consecutive_away(R, T) :- away_game(R, T), consecutive_away(R-1, T), R > 1.

% Forbid 4 consecutive home games
:- consecutive_home(R, T), R >= 4, consecutive_home(R-1, T), consecutive_home(R-2, T), consecutive_home(R-3, T).

% Forbid 4 consecutive away games
:- consecutive_away(R, T), R >= 4, consecutive_away(R-1, T), consecutive_away(R-2, T), consecutive_away(R-3, T).

% Constraint 5: Rivalry constraint - A and B cannot play in round 1
:- match(1, a, b).
:- match(1, b, a).

% C and D cannot play in round 1
:- match(1, c, d).
:- match(1, d, c).

% Constraint 6: Mandatory break - each team must have at least one sequence of 2 consecutive home games
has_home_stand(T) :- consecutive_home(R, T), consecutive_home(R-1, T), R > 1.
:- team(T), not has_home_stand(T).

% Constraint 7: Travel fatigue
% If travel distance > 140, must play home in next round
% Travel distance is from location at end of previous round to away venue
fatigue(R, T) :- away_game(R, T), location(R-1, T, Loc1), home_city(Opponent, Loc2), match(R, Opponent, T), dist(Loc1, Loc2, D), D > 140, R < 10.

% If fatigue, must play home in next round
:- fatigue(R, T), not home_game(R+1, T), R < 10.

% Show schedule
#show match/3.