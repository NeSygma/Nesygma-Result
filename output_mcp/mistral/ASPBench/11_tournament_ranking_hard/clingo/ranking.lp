% Domain declarations
team(t01). team(t02). team(t03). team(t04). team(t05). team(t06). team(t07). team(t08). team(t09). team(t10).
team(t11). team(t12). team(t13). team(t14). team(t15). team(t16). team(t17). team(t18). team(t19). team(t20).
team(t21). team(t22). team(t23). team(t24). team(t25). team(t26). team(t27). team(t28). team(t29). team(t30).

% Group definitions
% Group A: T01-T05
group(a, t01). group(a, t02). group(a, t03). group(a, t04). group(a, t05).
% Group B: T06-T10
group(b, t06). group(b, t07). group(b, t08). group(b, t09). group(b, t10).
% Group C: T11-T15
group(c, t11). group(c, t12). group(c, t13). group(c, t14). group(c, t15).
% Group D: T16-T20
group(d, t16). group(d, t17). group(d, t18). group(d, t19). group(d, t20).
% Group E: T21-T25
group(e, t21). group(e, t22). group(e, t23). group(e, t24). group(e, t25).
% Group F: T26-T30
group(f, t26). group(f, t27). group(f, t28). group(f, t29). group(f, t30).

% Seed teams (T01-T10)
seed(t01). seed(t02). seed(t03). seed(t04). seed(t05).
seed(t06). seed(t07). seed(t08). seed(t09). seed(t10).

% Position range (1 to 30)
position(1..30).

% Match results: beats(winner, loser, weight)
% Key matches that could cause violations
beats(t05, t18, 4). beats(t10, t11, 3). beats(t07, t28, 2). beats(t08, t19, 1). beats(t02, t27, 5).
beats(t04, t21, 3). beats(t03, t12, 2). beats(t06, t17, 4). beats(t09, t25, 1). beats(t01, t30, 5).
beats(t13, t29, 2). beats(t14, t20, 3). beats(t15, t16, 1). beats(t22, t08, 4). beats(t23, t03, 2).
beats(t24, t07, 3). beats(t26, t05, 1). beats(t25, t14, 5). beats(t20, t22, 2). beats(t28, t15, 3).

% Additional cross-group matches
beats(t01, t02, 2). beats(t02, t03, 1). beats(t03, t04, 3). beats(t04, t05, 2).
beats(t06, t07, 1). beats(t07, t08, 4). beats(t08, t09, 2). beats(t09, t10, 3).
beats(t11, t12, 2). beats(t12, t13, 1). beats(t13, t14, 3). beats(t14, t15, 2).
beats(t16, t17, 1). beats(t17, t18, 4). beats(t18, t19, 2). beats(t19, t20, 3).
beats(t21, t22, 2). beats(t22, t23, 1). beats(t23, t24, 3). beats(t24, t25, 2).
beats(t26, t27, 1). beats(t27, t28, 4). beats(t28, t29, 2). beats(t29, t30, 3).

beats(t01, t06, 3). beats(t02, t07, 2). beats(t03, t08, 1). beats(t04, t09, 5). beats(t05, t10, 4).
beats(t06, t11, 3). beats(t07, t12, 2). beats(t08, t13, 1). beats(t09, t14, 5). beats(t10, t15, 4).
beats(t11, t16, 3). beats(t12, t17, 2). beats(t13, t18, 1). beats(t14, t19, 5). beats(t15, t20, 4).
beats(t16, t21, 3). beats(t17, t22, 2). beats(t18, t23, 1). beats(t19, t24, 5). beats(t20, t25, 4).
beats(t21, t26, 3). beats(t22, t27, 2). beats(t23, t28, 1). beats(t24, t29, 5). beats(t25, t30, 4).

% Choice rule: assign each team to exactly one rank
{rank(T, R) : position(R)} = 1 :- team(T).

% Uniqueness: each rank has exactly one team
{rank(T, R)} = 1 :- position(R).

% Derive "above" relation: T1 is above T2 if T1 has a lower rank number
above(T1, T2) :- rank(T1, R1), rank(T2, R2), R1 < R2.

% Calculate violations: when a lower-ranked team beats a higher-ranked team
violation(T1, T2, W) :- above(T2, T1), beats(T1, T2, W).

% Total violation count
total_violation(V) :- V = #sum { W, T1, T2 : violation(T1, T2, W) }.

% --- Hard Constraints ---

% 1. Must-above constraints (20 pairs)
:- above(T2, T1), must_above(T1, T2).

% Define must_above facts
must_above(t05, t18). must_above(t10, t11). must_above(t07, t28). must_above(t08, t19).
must_above(t02, t27). must_above(t04, t21). must_above(t03, t12). must_above(t06, t17).
must_above(t09, t25). must_above(t01, t30). must_above(t13, t29). must_above(t14, t20).
must_above(t15, t16). must_above(t22, t08). must_above(t23, t03). must_above(t24, t07).
must_above(t26, t05). must_above(t25, t14). must_above(t20, t22). must_above(t28, t15).

% 2. Adjacency bans (15 pairs): teams cannot be adjacent in ranking
:- rank(T1, R), rank(T2, R+1), adjacent_ban(T1, T2).
:- rank(T2, R), rank(T1, R+1), adjacent_ban(T1, T2).

% Define adjacent_ban facts
adjacent_ban(t02, t03). adjacent_ban(t04, t05). adjacent_ban(t06, t07). adjacent_ban(t08, t09).
adjacent_ban(t10, t11). adjacent_ban(t12, t13). adjacent_ban(t14, t15). adjacent_ban(t16, t17).
adjacent_ban(t18, t19). adjacent_ban(t20, t21). adjacent_ban(t22, t23). adjacent_ban(t24, t25).
adjacent_ban(t26, t27). adjacent_ban(t28, t29). adjacent_ban(t01, t30).

% 3. Forbid-top constraints (8 teams)
% T27 cannot be in top 3
:- rank(t27, R), R = 1.
:- rank(t27, R), R = 2.
:- rank(t27, R), R = 3.

% T14 cannot be in top 5
:- rank(t14, R), R = 1.
:- rank(t14, R), R = 2.
:- rank(t14, R), R = 3.
:- rank(t14, R), R = 4.
:- rank(t14, R), R = 5.

% T18 cannot be in top 4
:- rank(t18, R), R = 1.
:- rank(t18, R), R = 2.
:- rank(t18, R), R = 3.
:- rank(t18, R), R = 4.

% T21 cannot be in top 2
:- rank(t21, R), R = 1.
:- rank(t21, R), R = 2.

% T22 cannot be in top 6
:- rank(t22, R), R = 1.
:- rank(t22, R), R = 2.
:- rank(t22, R), R = 3.
:- rank(t22, R), R = 4.
:- rank(t22, R), R = 5.
:- rank(t22, R), R = 6.

% T19 cannot be in top 8
:- rank(t19, R), R = 1.
:- rank(t19, R), R = 2.
:- rank(t19, R), R = 3.
:- rank(t19, R), R = 4.
:- rank(t19, R), R = 5.
:- rank(t19, R), R = 6.
:- rank(t19, R), R = 7.
:- rank(t19, R), R = 8.

% T16 cannot be in top 7
:- rank(t16, R), R = 1.
:- rank(t16, R), R = 2.
:- rank(t16, R), R = 3.
:- rank(t16, R), R = 4.
:- rank(t16, R), R = 5.
:- rank(t16, R), R = 6.
:- rank(t16, R), R = 7.

% T29 cannot be in top 10
:- rank(t29, R), R = 1.
:- rank(t29, R), R = 2.
:- rank(t29, R), R = 3.
:- rank(t29, R), R = 4.
:- rank(t29, R), R = 5.
:- rank(t29, R), R = 6.
:- rank(t29, R), R = 7.
:- rank(t29, R), R = 8.
:- rank(t29, R), R = 9.
:- rank(t29, R), R = 10.

% 4. Forbid-block constraints (5 teams)
% T14 cannot be in positions 11-15
:- rank(t14, R), R >= 11, R =< 15.

% T20 cannot be in positions 5-9
:- rank(t20, R), R >= 5, R =< 9.

% T23 cannot be in positions 13-17
:- rank(t23, R), R >= 13, R =< 17.

% T02 cannot be in positions 21-25
:- rank(t02, R), R >= 21, R =< 25.

% T09 cannot be in positions 26-30
:- rank(t09, R), R >= 26, R =< 30.

% 5. Diversity constraint: In any consecutive window of 5 teams, no more than 2 teams from the same group
% Define windows: positions 1-5, 2-6, ..., 26-30
window(R) :- position(R), R <= 26.

% For each window, count teams per group
group_in_window(G, R) :- window(R), group(G, T), rank(T, Pos), Pos >= R, Pos =< R+4.

% Constrain that no group has more than 2 teams in any window
:- window(R), group(G, _), #count { T : group_in_window(G, R) } > 2.

% 6. Seed quota: At least 6 seed teams (T01-T10) must be in the top 10 positions
:- #count { T, R : seed(T), rank(T, R), R =< 10 } < 6.

% 7. Violation bound: Total weighted violations must be ≤ 650
:- total_violation(V), V > 650.

% --- Show directives ---
#show rank/2.
#show total_violation/1.