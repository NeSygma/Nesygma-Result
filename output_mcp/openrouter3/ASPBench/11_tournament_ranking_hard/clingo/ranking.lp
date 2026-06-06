% Teams and Groups
team(T01). team(T02). team(T03). team(T04). team(T05).
team(T06). team(T07). team(T08). team(T09). team(T10).
team(T11). team(T12). team(T13). team(T14). team(T15).
team(T16). team(T17). team(T18). team(T19). team(T20).
team(T21). team(T22). team(T23). team(T24). team(T25).
team(T26). team(T27). team(T28). team(T29). team(T30).

% Groups
group(a, T01). group(a, T02). group(a, T03). group(a, T04). group(a, T05).
group(b, T06). group(b, T07). group(b, T08). group(b, T09). group(b, T10).
group(c, T11). group(c, T12). group(c, T13). group(c, T14). group(c, T15).
group(d, T16). group(d, T17). group(d, T18). group(d, T19). group(d, T20).
group(e, T21). group(e, T22). group(e, T23). group(e, T24). group(e, T25).
group(f, T26). group(f, T27). group(f, T28). group(f, T29). group(f, T30).

% Seeds (T01-T10)
seed(T01). seed(T02). seed(T03). seed(T04). seed(T05).
seed(T06). seed(T07). seed(T08). seed(T09). seed(T10).

% Positions 1-30
position(1..30).

% Generate match results based on the pattern
% For each pair (i,j) where i < j, determine winner based on (i+j) mod 2
% We need to map team indices to numbers 0-29
team_index(T01, 0). team_index(T02, 1). team_index(T03, 2). team_index(T04, 3). team_index(T05, 4).
team_index(T06, 5). team_index(T07, 6). team_index(T08, 7). team_index(T09, 8). team_index(T10, 9).
team_index(T11, 10). team_index(T12, 11). team_index(T13, 12). team_index(T14, 13). team_index(T15, 14).
team_index(T16, 15). team_index(T17, 16). team_index(T18, 17). team_index(T19, 18). team_index(T20, 19).
team_index(T21, 20). team_index(T22, 21). team_index(T23, 22). team_index(T24, 23). team_index(T25, 24).
team_index(T26, 25). team_index(T27, 26). team_index(T28, 27). team_index(T29, 28). team_index(T30, 29).

% Generate weights (1-5) using a deterministic pattern based on team indices
% For reproducibility, we'll use a simple hash function
weight(T1, T2, W) :-
    team_index(T1, I1),
    team_index(T2, I2),
    I1 < I2,
    W = ((I1 * 31 + I2) mod 5) + 1.

% Determine winner based on (i+j) mod 2
% If (i+j) mod 2 == 0, team with lower index wins
% If (i+j) mod 2 == 1, team with higher index wins
beats(T1, T2, W) :-
    team_index(T1, I1),
    team_index(T2, I2),
    I1 < I2,
    weight(T1, T2, W),
    (I1 + I2) mod 2 == 0.

beats(T2, T1, W) :-
    team_index(T1, I1),
    team_index(T2, I2),
    I1 < I2,
    weight(T1, T2, W),
    (I1 + I2) mod 2 == 1.

% Ranking: each team gets exactly one position
1 { rank(T, P) : position(P) } 1 :- team(T).

% Each position gets exactly one team
1 { rank(T, P) : team(T) } 1 :- position(P).

% Must-above constraints
:- rank(T1, P1), rank(T2, P2), must_above(T1, T2), P1 >= P2.

must_above(T05, T18).
must_above(T10, T11).
must_above(T07, T28).
must_above(T08, T19).
must_above(T02, T27).
must_above(T04, T21).
must_above(T03, T12).
must_above(T06, T17).
must_above(T09, T25).
must_above(T01, T30).
must_above(T13, T29).
must_above(T14, T20).
must_above(T15, T16).
must_above(T22, T08).
must_above(T23, T03).
must_above(T24, T07).
must_above(T26, T05).
must_above(T25, T14).
must_above(T20, T22).
must_above(T28, T15).

% Adjacency bans
:- rank(T1, P), rank(T2, P+1), adjacent_ban(T1, T2).
:- rank(T1, P+1), rank(T2, P), adjacent_ban(T1, T2).

adjacent_ban(T02, T03).
adjacent_ban(T04, T05).
adjacent_ban(T06, T07).
adjacent_ban(T08, T09).
adjacent_ban(T10, T11).
adjacent_ban(T12, T13).
adjacent_ban(T14, T15).
adjacent_ban(T16, T17).
adjacent_ban(T18, T19).
adjacent_ban(T20, T21).
adjacent_ban(T22, T23).
adjacent_ban(T24, T25).
adjacent_ban(T26, T27).
adjacent_ban(T28, T29).
adjacent_ban(T01, T30).

% Forbid-top constraints
:- rank(T27, P), P <= 3.
:- rank(T14, P), P <= 5.
:- rank(T18, P), P <= 4.
:- rank(T21, P), P <= 2.
:- rank(T22, P), P <= 6.
:- rank(T19, P), P <= 8.
:- rank(T16, P), P <= 7.
:- rank(T29, P), P <= 10.

% Forbid-block constraints
:- rank(T14, P), P >= 11, P <= 15.
:- rank(T20, P), P >= 5, P <= 9.
:- rank(T23, P), P >= 13, P <= 17.
:- rank(T02, P), P >= 21, P <= 25.
:- rank(T09, P), P >= 26, P <= 30.

% Diversity constraint: In any consecutive window of 5 teams, no more than 2 from same group
% For each position P, consider window P..P+4
% Count teams from each group in the window
% If any group has > 2 teams in the window, it's invalid
:- position(P), P <= 26,
   group(G, T1), group(G, T2), group(G, T3), group(G, T4),
   rank(T1, P1), rank(T2, P2), rank(T3, P3), rank(T4, P4),
   P1 >= P, P1 <= P+4,
   P2 >= P, P2 <= P+4,
   P3 >= P, P3 <= P+4,
   P4 >= P, P4 <= P+4,
   T1 != T2, T1 != T3, T1 != T4, T2 != T3, T2 != T4, T3 != T4.

% Seed quota: At least 6 seed teams in top 10
seed_top10_count(N) :-
    N = #count{ T : seed(T), rank(T, P), P <= 10 }.
:- seed_top10_count(N), N < 6.

% Violation calculation
% A violation occurs when a lower-ranked team beat a higher-ranked team
% For each match where T1 beats T2, if rank(T1) > rank(T2), it's a violation
violation(T1, T2, W) :-
    beats(T1, T2, W),
    rank(T1, P1),
    rank(T2, P2),
    P1 > P2.

total_violations(V) :-
    V = #sum{ W, T1, T2 : violation(T1, T2, W) }.

% Violation bound
:- total_violations(V), V > 650.

% Show the ranking and violations
#show rank/2.
#show total_violations/1.
#show seed_top10_count/1.