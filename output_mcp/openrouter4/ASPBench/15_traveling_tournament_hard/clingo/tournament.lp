% Teams
team("A"; "B"; "C"; "D"; "E"; "F").

% Rounds
round(1..10).

% Distance matrix (scaled by 10)
dist("A","B",100). dist("A","C",94). dist("A","D",150). dist("A","E",180). dist("A","F",170).
dist("B","C",94). dist("B","D",180). dist("B","E",150). dist("B","F",94).
dist("C","D",86). dist("C","E",86). dist("C","F",100).
dist("D","E",100). dist("D","F",170).
dist("E","F",94).

% Symmetric distances
dist(T2, T1, D) :- dist(T1, T2, D).

% Initial location before round 1
init_loc(T, T) :- team(T).

% Choice: exactly one round for each ordered pair (home team, away team)
1 { match(R, T1, T2) : round(R) } 1 :- team(T1), team(T2), T1 != T2.

% Each team plays exactly once per round
:- team(T), round(R), { match(R, T, _) ; match(R, _, T) } != 1.

% --- Derived predicates ---
home_game(R, T) :- match(R, T, _).
away_game(R, T) :- match(R, _, T).

% --- Location tracking ---
% Location at the end of round R
loc_after(T, R, T) :- match(R, T, _), round(R).
loc_after(T, R, H) :- match(R, H, T), round(R).

% Location before round R (for fatigue calculation)
loc_before(T, 1, T) :- team(T).
loc_before(T, R, City) :- round(R), R > 1, loc_after(T, R-1, City).

% --- Constraint 4: Consecutive Game Limit ---
% No team may play 4 consecutive home games
:- team(T), round(R), R <= 7,
   home_game(R, T), home_game(R+1, T), home_game(R+2, T), home_game(R+3, T).

% No team may play 4 consecutive away games
:- team(T), round(R), R <= 7,
   away_game(R, T), away_game(R+1, T), away_game(R+2, T), away_game(R+3, T).

% --- Constraint 5: Rivalry Constraint ---
:- match(1, "A", "B").
:- match(1, "B", "A").
:- match(1, "C", "D").
:- match(1, "D", "C").

% --- Constraint 6: Mandatory Break ---
% Each team must have at least one sequence of two consecutive home games
has_home_stand(T) :- home_game(R, T), home_game(R+1, T), round(R), R < 10.
:- team(T), not has_home_stand(T).

% --- Constraint 7: Travel Fatigue ---
% If travel distance > 140 to reach an away game, must play at home next round
:- team(T), round(R), R < 10,
   match(R, H, T),
   loc_before(T, R, PrevCity),
   dist(PrevCity, H, D),
   D > 140,
   not home_game(R+1, T).

% --- Show schedule ---
#show match/3.