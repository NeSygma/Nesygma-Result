% Define the houses and positions
house(j). house(k). house(l). house(m). house(n). house(o). house(p).
position(1..7).

% Define time of day
time_of_day(morning). time_of_day(afternoon). time_of_day(evening).

% Assign positions to time slots
time_of(P, morning) :- position(P), P = 1..2.
time_of(P, afternoon) :- position(P), P = 3..5.
time_of(P, evening) :- position(P), P = 6..7.

% Define the sequences for each option as facts
% Option A: K, o, L, M, N, J, P
seq(a, 1, k). seq(a, 2, o). seq(a, 3, l). seq(a, 4, m). seq(a, 5, n). seq(a, 6, j). seq(a, 7, p).
% Option B: N, L, P, K, M, o, J
seq(b, 1, n). seq(b, 2, l). seq(b, 3, p). seq(b, 4, k). seq(b, 5, m). seq(b, 6, o). seq(b, 7, j).
% Option C: o, P, K, L, N, M, J
seq(c, 1, o). seq(c, 2, p). seq(c, 3, k). seq(c, 4, l). seq(c, 5, n). seq(c, 6, m). seq(c, 7, j).
% Option D: o, P, M, N, K, L, J
seq(d, 1, o). seq(d, 2, p). seq(d, 3, m). seq(d, 4, n). seq(d, 5, k). seq(d, 6, l). seq(d, 7, j).
% Option E: P, o, K, J, L, N, M
seq(e, 1, p). seq(e, 2, o). seq(e, 3, k). seq(e, 4, j). seq(e, 5, l). seq(e, 6, n). seq(e, 7, m).

% Constraint 1: J must be shown in the evening (positions 6 or 7)
:- seq(Opt, P, j), time_of(P, T), T != evening.

% Constraint 2: K cannot be shown in the morning (positions 1 or 2)
:- seq(Opt, P, k), time_of(P, morning).

% Constraint 3: L must be shown after K and before M (K < L < M)
:- seq(Opt, PK, k), seq(Opt, PL, l), seq(Opt, PM, m), PL =< PK.
:- seq(Opt, PK, k), seq(Opt, PL, l), seq(Opt, PM, m), PM =< PL.

% Ensure all houses are assigned exactly once in each sequence
% No duplicate houses in the same position
:- seq(Opt, P, H1), seq(Opt, P, H2), H1 != H2.
% All houses must appear exactly once in the sequence
:- house(H), not seq(_, _, H).

% Map the correct answer to option/1
option(a) :- seq(a, _, _).
option(b) :- seq(b, _, _).
option(c) :- seq(c, _, _).
option(d) :- seq(d, _, _).
option(e) :- seq(e, _, _).

#show option/1.