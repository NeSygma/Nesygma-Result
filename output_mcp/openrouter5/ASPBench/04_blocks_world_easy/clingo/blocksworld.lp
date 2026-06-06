%%% Blocks World Planning - Find shortest sequence of moves

%%% DOMAIN DEFINITION
block(a; b; c).
position(P) :- block(P).
position(table).

% Time horizon - we know optimal is 3 moves, so we need at most 3 steps
% plus initial state at time 0
time(0..3).

%%% INITIAL STATE
% Block A is on the table at time 0
on(a, table, 0).
% Block B is on the table at time 0
on(b, table, 0).
% Block C is on top of block A at time 0
on(c, a, 0).

%%% GOAL STATE (at final time T)
goal_on(a, b).
goal_on(b, c).
goal_on(c, table).

%%% HELPER: Clear block (nothing on top)
clear(X, T) :- block(X), time(T), not on(_, X, T).

%%% HELPER: Block is on something (either table or another block)
on_something(X, T) :- on(X, P, T), block(X), time(T).

%%% CONSTRAINTS ON STATE

% 1. Each block can only be in one position at each time
:- on(X, P1, T), on(X, P2, T), P1 != P2, block(X), time(T).

% 2. At most one block can be on top of another block
:- on(X1, Y, T), on(X2, Y, T), X1 != X2, block(Y), time(T).

% 3. No block can be placed on itself
:- on(X, X, T), time(T).

% 4. If X is on Y at time T, then Y must be clear at time T (except table)
:- on(X, Y, T), block(Y), time(T), not clear(Y, T).

% 5. Every block must be on exactly one thing at each time
:- block(X), time(T), not on_something(X, T).

%%% ACTION GENERATION
% At each time step T (0 to max_time-1), we can move exactly one clear block
% to a position (table or another clear block)
% The block being moved must be clear at time T
% The target position must be clear at time T (if it's a block)
% The block cannot be moved to itself

% Choice: at each time step, move exactly one block
1 { move(X, To, T) : block(X), position(To), X != To, clear(X, T), 
    (To = table; block(To), clear(To, T)) } 1 :- time(T), T < 3.

%%% ACTION EFFECTS
% If block X is moved to position To at time T, then at time T+1, X is on To
on(X, To, T+1) :- move(X, To, T), time(T), T < 3.

%%% FRAME AXIOMS (Persistence)
% If block X was on P at time T and X was not moved at time T, then X is still on P at T+1
on(X, P, T+1) :- on(X, P, T), time(T), T < 3, not move(X, _, T).

%%% GOAL ACHIEVEMENT
% The goal must be satisfied at the final time (time 3)
:- goal_on(X, P), not on(X, P, 3).

%%% OUTPUT
#show move/3.
#show plan_length/1.
#show step/3.

% Derive plan length
plan_length(N) :- N = #count{T : move(_, _, T)}.

% Derive step-by-step actions
step(N, X, To) :- move(X, To, T), N = T + 1.