% Tournament Scheduling Problem - Debug Version

% ===== 1. TEAMS AND LOCATIONS =====
team(a). team(b). team(c). team(d). team(e). team(f).

% Coordinates (x, y) - scaled by 10
location(a, 0, 0).
location(b, 10, 0).
location(c, 5, 8).
location(d, 0, 15).
location(e, 10, 15).
location(f, 15, 8).

% ===== 2. DISTANCE MATRIX =====
% Euclidean distances scaled by 10 (precomputed)
distance(a, b, 100). distance(b, a, 100).
distance(a, c, 94). distance(c, a, 94).
distance(a, d, 150). distance(d, a, 150).
distance(a, e, 180). distance(e, a, 180).
distance(a, f, 170). distance(f, a, 170).
distance(b, c, 94). distance(c, b, 94).
distance(b, d, 180). distance(d, b, 180).
distance(b, e, 150). distance(e, b, 150).
distance(b, f, 94). distance(f, b, 94).
distance(c, d, 86). distance(d, c, 86).
distance(c, e, 86). distance(e, c, 86).
distance(c, f, 100). distance(f, c, 100).
distance(d, e, 100). distance(e, d, 100).
distance(d, f, 170). distance(f, d, 170).
distance(e, f, 94). distance(f, e, 94).

% ===== 3. ROUNDS AND TIME =====
round(1..10).

% ===== 4. MATCH SCHEDULING =====
% Each match is defined by: round, home team, away team
% We need exactly 3 matches per round
{ match(R, H, A) : team(H), team(A), H != A } 3 :- round(R).

% ===== 5. DOUBLE ROUND-ROBIN CONSTRAINT =====
% Each ordered pair (H, A) with H != A must play exactly once
1 { match(R, H, A) : round(R) } 1 :- team(H), team(A), H != A.

% ===== 6. EACH TEAM PLAYS EXACTLY ONCE PER ROUND =====
% Each team plays exactly once per round (either home or away)
1 { match(R, H, A) : team(A), H != A } 1 :- round(R), team(H).
1 { match(R, H, A) : team(H), H != A } 1 :- round(R), team(A).

% ===== 7. STATEFUL TRAVEL TRACKING =====
% Location of team at end of each round
% Initial location: at home before round 1
location_at_end(1, T, X, Y) :- team(T), location(T, X, Y).

% After round R, team's location depends on whether they played home or away
location_at_end(R+1, T, X, Y) :- 
    round(R), team(T),
    match(R, T, A),  % Team T played at home
    location(T, X, Y).

location_at_end(R+1, T, X, Y) :- 
    round(R), team(T),
    match(R, H, T),  % Team T played away
    location(H, X, Y).

% ===== 8. CONSECUTIVE GAME LIMIT =====
% Track consecutive home/away games
% Home streak: count consecutive home games ending at round R
home_streak(R, T, 1) :- round(R), team(T),
    match(R, T, _),  % Home game at R
    not match(R-1, T, _).  % Not home at R-1

home_streak(R, T, N) :- round(R), team(T),
    match(R, T, _),  % Home game at R
    home_streak(R-1, T, N-1),  % Previous streak
    N <= 3.

% Away streak: count consecutive away games ending at round R
away_streak(R, T, 1) :- round(R), team(T),
    match(R, _, T),  % Away game at R
    not match(R-1, _, T).  % Not away at R-1

away_streak(R, T, N) :- round(R), team(T),
    match(R, _, T),  % Away game at R
    away_streak(R-1, T, N-1),  % Previous streak
    N <= 3.

% Constraint: No more than 3 consecutive home or away games
:- home_streak(R, T, N), N > 3.
:- away_streak(R, T, N), N > 3.

% ===== 9. RIVALRY CONSTRAINTS =====
% Teams A and B cannot play each other in round 1
:- match(1, a, b).
:- match(1, b, a).

% Teams C and D cannot play each other in round 1
:- match(1, c, d).
:- match(1, d, c).

% ===== 10. MANDATORY BREAK (HOME STAND) =====
% Each team must have at least one sequence of two consecutive home games
has_home_stand(T) :- team(T), round(R), 
    match(R, T, _), match(R+1, T, _).

:- team(T), not has_home_stand(T).

% ===== 11. TRAVEL FATIGUE CONSTRAINT =====
% If a team travels > 140 to reach an away game, they must play home in the next round
% Distance is calculated from team's location at end of previous round to away venue

% Helper: distance from team's location at end of round R to away venue at round R+1
travel_distance(R, T, D) :- 
    round(R), team(T),
    match(R+1, H, T),  % Team T plays away at round R+1 at H's venue
    location_at_end(R, T, X1, Y1),  % Team T's location at end of round R
    location(H, X2, Y2),  % Home venue of opponent H
    distance_from_coords(X1, Y1, X2, Y2, D).

% Calculate Euclidean distance from coordinates (precomputed)
distance_from_coords(0, 0, 10, 0, 100).
distance_from_coords(0, 0, 5, 8, 94).
distance_from_coords(0, 0, 0, 15, 150).
distance_from_coords(0, 0, 10, 15, 180).
distance_from_coords(0, 0, 15, 8, 170).
distance_from_coords(10, 0, 5, 8, 94).
distance_from_coords(10, 0, 0, 15, 180).
distance_from_coords(10, 0, 10, 15, 150).
distance_from_coords(10, 0, 15, 8, 94).
distance_from_coords(5, 8, 0, 15, 86).
distance_from_coords(5, 8, 10, 15, 86).
distance_from_coords(5, 8, 15, 8, 100).
distance_from_coords(0, 15, 10, 15, 100).
distance_from_coords(0, 15, 15, 8, 170).
distance_from_coords(10, 15, 15, 8, 94).

% Fatigue constraint: if travel distance > 140, team must play home next round
% This means: if team T plays away at round R+1 with distance > 140,
% then at round R+2, team T must play at home (if R+2 <= 10)
:- round(R), R <= 9, team(T),
    match(R+1, H, T),  % T plays away at R+1
    travel_distance(R, T, D), D > 140,
    not match(R+2, T, _).  % T must play home at R+2

% ===== 12. VALIDATION CONSTRAINTS =====
% Ensure no team plays against itself
:- match(_, T, T).

% Ensure each round has exactly 3 matches
:- round(R), #count{H, A : match(R, H, A)} != 3.

% ===== 13. OUTPUT =====
#show match/3.
#show location_at_end/4.