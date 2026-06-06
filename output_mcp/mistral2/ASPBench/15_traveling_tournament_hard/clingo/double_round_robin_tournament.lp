% --- Fixed Data ---
team(a; b; c; d; e; f).
home_location(a, 0, 0).
home_location(b, 10, 0).
home_location(c, 5, 8).
home_location(d, 0, 15).
home_location(e, 10, 15).
home_location(f, 15, 8).

distance(a, b, 100). distance(a, c, 94). distance(a, d, 150). distance(a, e, 180). distance(a, f, 170).
distance(b, a, 100). distance(b, c, 94). distance(b, d, 180). distance(b, e, 150). distance(b, f, 94).
distance(c, a, 94). distance(c, b, 94). distance(c, d, 86). distance(c, e, 86). distance(c, f, 100).
distance(d, a, 150). distance(d, b, 180). distance(d, c, 86). distance(d, e, 100). distance(d, f, 170).
distance(e, a, 180). distance(e, b, 150). distance(e, c, 86). distance(e, d, 100). distance(e, f, 94).
distance(f, a, 170). distance(f, b, 94). distance(f, c, 100). distance(f, d, 170). distance(f, e, 94).

round(0..9).

% --- Match Generation ---
% Each ordered pair (T1, T2) plays exactly once (home/away)
1 { match(R, H, A) : round(R), team(H), team(A), H != A } 10 :- team(H), team(A), H != A.

% Each round has exactly 3 matches
:- round(R), #count{ H, A : match(R, H, A) } != 3.

% No duplicate matches in the same round
:- round(R), match(R, H1, A1), match(R, H2, A2), (H1, A1) != (H2, A2).

% --- Stateful Location ---
% Initial location (round 0) is home city
location(T, 0, X, Y) :- home_location(T, X, Y).

% Location after round R is:
% - Home location if played at home in round R
% - Away team's home location if played away in round R
location(T, R, X, Y) :-
    match(R, T, _),
    home_location(T, X, Y),
    round(R).
location(T, R, X, Y) :-
    match(R, _, T),
    home_location(T, X, Y),
    round(R).

% --- Consecutive Home/Away Games ---
% Track consecutive home/away games
consecutive_home(T, R, 1) :-
    match(R, T, _),
    round(R),
    not consecutive_home(T, R-1, _).
consecutive_home(T, R, N) :-
    match(R, T, _),
    match(R-1, T, _),
    consecutive_home(T, R-1, N-1),
    N > 1,
    round(R).
consecutive_away(T, R, 1) :-
    match(R, _, T),
    round(R),
    not consecutive_away(T, R-1, _).
consecutive_away(T, R, N) :-
    match(R, _, T),
    match(R-1, _, T),
    consecutive_away(T, R-1, N-1),
    N > 1,
    round(R).

% No more than 3 consecutive home/away games
:- team(T), round(R), consecutive_home(T, R, N), N > 3.
:- team(T), round(R), consecutive_away(T, R, N), N > 3.

% --- Travel Fatigue ---
% If a team played away in round R and the distance from their location at the end of round R-1 to the away venue > 140,
% then they must play at home in round R+1 (if R+1 exists)
travel_fatigue(T, R) :-
    match(R, _, T),
    round(R),
    R < 9,
    location(T, R-1, X1, Y1),
    home_location(Opp, X2, Y2),
    match(R, _, Opp),
    distance(T, Opp, D),
    D > 140.
:- travel_fatigue(T, R), match(R+1, T, _).

% --- Rivalry Constraints ---
:- match(1, a, b).
:- match(1, b, a).
:- match(1, c, d).
:- match(1, d, c).

% --- Mandatory Home Stand ---
% Each team must have at least one home stand (two consecutive home games)
home_stand(T, R) :-
    match(R, T, _),
    match(R-1, T, _),
    round(R),
    round(R-1).
:- team(T), not home_stand(T, _).

% --- Show Schedule ---
#show match/3.