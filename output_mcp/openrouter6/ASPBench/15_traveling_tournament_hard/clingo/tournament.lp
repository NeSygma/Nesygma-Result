% Tournament Scheduling for 6 teams over 10 rounds

% ====== DOMAIN DEFINITIONS ======
team(a). team(b). team(c). team(d). team(e). team(f).
round(1..10).

% ====== DISTANCE MATRIX (scaled by 10) ======
% Distance between home cities of teams
dist(a, b, 100). dist(b, a, 100).
dist(a, c, 94).  dist(c, a, 94).
dist(a, d, 150). dist(d, a, 150).
dist(a, e, 180). dist(e, a, 180).
dist(a, f, 170). dist(f, a, 170).
dist(b, c, 94).  dist(c, b, 94).
dist(b, d, 180). dist(d, b, 180).
dist(b, e, 150). dist(e, b, 150).
dist(b, f, 94).  dist(f, b, 94).
dist(c, d, 86).  dist(d, c, 86).
dist(c, e, 86).  dist(e, c, 86).
dist(c, f, 100). dist(f, c, 100).
dist(d, e, 100). dist(e, d, 100).
dist(d, f, 170). dist(f, d, 170).
dist(e, f, 94).  dist(f, e, 94).

% ====== MATCH GENERATION ======
% For each round, choose exactly 3 matches (each team plays exactly once)
% Each match is represented as match(R, Home, Away) where Home != Away
{ match(R, H, A) : team(A), A != H } 1 :- round(R), team(H).

% Ensure exactly 3 matches per round (6 teams / 2 = 3 matches)
:- round(R), #count{ H, A : match(R, H, A) } != 3.

% ====== DOUBLE ROUND-ROBIN CONSTRAINT ======
% Each ordered pair (H, A) with H != A must play exactly once
:- team(H), team(A), H != A, #count{ R : match(R, H, A) } != 1.

% ====== HOME/AWAY DERIVATIONS ======
is_home(R, T) :- match(R, T, A).
is_away(R, T) :- match(R, H, T).

% ====== STATEFUL TRAVEL TRACKING ======
% location_team(T, R, U): After round R, team T is at team U's home city
% Initial state (before round 1): each team at its own home
location_team(T, 0, T) :- team(T).

% After each round: home team stays home, away team goes to home team's city
location_team(T, R, T) :- match(R, T, A).  % T is home
location_team(T, R, H) :- match(R, H, T).  % T is away

% ====== CONSECUTIVE GAME LIMIT ======
% No team may play more than 3 consecutive home or away games
:- team(T), round(R), R <= 7,
   is_home(R, T), is_home(R+1, T), is_home(R+2, T), is_home(R+3, T).
:- team(T), round(R), R <= 7,
   is_away(R, T), is_away(R+1, T), is_away(R+2, T), is_away(R+3, T).

% ====== RIVALRY CONSTRAINT ======
% A and B cannot play each other in round 1
:- match(1, a, b).
:- match(1, b, a).
% C and D cannot play each other in round 1
:- match(1, c, d).
:- match(1, d, c).

% ====== MANDATORY BREAK ======
% Each team must have at least one sequence of two consecutive home games
has_two_consecutive_home(T) :- team(T), round(R), R <= 9,
                               is_home(R, T), is_home(R+1, T).
:- team(T), not has_two_consecutive_home(T).

% ====== TRAVEL FATIGUE CONSTRAINT ======
% If a team travels > 140 to an away game, must play home next round
:- match(R, H, T), R <= 9,  % R from 1 to 9 (need next round)
   location_team(T, R-1, U),  % T's location after previous round
   dist(U, H, D), D > 140,    % distance from previous location to away venue
   not is_home(R+1, T).       % must play home in next round

% ====== OUTPUT ======
#show match/3.
#show is_home/2.
#show is_away/2.