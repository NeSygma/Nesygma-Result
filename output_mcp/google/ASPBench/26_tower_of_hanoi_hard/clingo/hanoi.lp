% Constants and Domains
disk(1..4).
peg(a; b; c; d).

% Time horizon
#const max_moves = 19.
time(0..max_moves).

% Initial State
at(D, a, 0) :- disk(D).

% Movement Choice
1 { move(D, F, T, Time) : disk(D), peg(F), peg(T), F != T } 1 :- time(Time), Time > 0.

% Preconditions
% 1. Only top disk can move
is_top(P, D, T) :- at(D, P, T), not at_smaller(D, P, T).
at_smaller(D, P, T) :- at(D, P, T), at(D2, P, T), D2 < D.

:- move(D, F, T, Time), not is_top(F, D, Time-1).

% 2. Larger on smaller
:- move(D, F, T, Time), is_top(T, D2, Time-1), D > D2.

% Effects
at(D, T, Time) :- move(D, F, T, Time).
at(D, P, Time) :- at(D, P, Time-1), not move(D, P, _, Time), time(Time), Time > 0.

% Integrity: A disk cannot be on two pegs
:- at(D, P1, Time), at(D, P2, Time), P1 != P2.

% Pilgrim's Journey: Every disk must land on B and C
landed(D, P, Time) :- move(D, _, P, Time).
visited(D, P, Time) :- landed(D, P, Time).
visited(D, P, Time) :- visited(D, P, Time-1), time(Time), Time > 0.

:- disk(D), not visited(D, b, max_moves).
:- disk(D), not visited(D, c, max_moves).

% Goal State
:- disk(D), not at(D, d, max_moves).

% Optimization
#minimize { 1, Time : move(D, F, T, Time) }.

% Output
#show move/4.
#show total_moves/0.
total_moves :- max_moves = M, #count { Time : move(_, _, _, Time) } = M.
#show total_moves/0.