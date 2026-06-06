% Blocks World Planning Problem

% Domain declarations
block(a). block(b). block(c).
position(X) :- block(X).
position(table).

% Time horizon (we expect 3 moves, so 4 time steps including initial state)
time(0..3).

% Initial state (time 0)
on(a, table, 0).
on(b, table, 0).
on(c, a, 0).

% Goal state conditions (must hold at final time)
goal_on(a, b).
goal_on(b, c).
goal_on(c, table).

% Clear blocks: a block is clear if nothing is on top of it
clear(X, T) :- block(X), time(T), not on(_, X, T).

% Each block has exactly one position at each time
1 { on(X, P, T) : position(P) } 1 :- block(X), time(T).

% At most one block can be on top of another block (except table)
:- on(X1, B, T), on(X2, B, T), X1 != X2, block(B).

% No block can be placed on itself
:- on(X, X, T).

% Move actions: choice rule for possible moves
{ move(B, From, To, T) : position(From), position(To) } 1 :- block(B), time(T), T < 3.

% Precondition: only clear blocks can be moved
:- move(B, From, To, T), not clear(B, T).

% Precondition: block must be at From position before move
:- move(B, From, To, T), not on(B, From, T).

% Precondition: cannot move to same position
:- move(B, From, To, T), From = To.

% Precondition: cannot place block on itself
:- move(B, From, To, T), B = To.

% Precondition: target position must be clear (if not table)
:- move(B, From, To, T), To != table, not clear(To, T).

% Effect: after move, block is at new position
on(B, To, T+1) :- move(B, From, To, T), time(T+1).

% Frame axiom: blocks not moved stay in same position
on(X, P, T+1) :- on(X, P, T), time(T), time(T+1), not move(X, _, _, T).

% Exactly one block moves per time step
:- time(T), T < 3, #count{ B : move(B, _, _, T) } != 1.

% Goal state must be reached at final time
:- on(a, P_a, 3), goal_on(a, Goal_a), P_a != Goal_a.
:- on(b, P_b, 3), goal_on(b, Goal_b), P_b != Goal_b.
:- on(c, P_c, 3), goal_on(c, Goal_c), P_c != Goal_c.

% Minimize number of moves (plan length)
#minimize { 1, T : move(_, _, _, T) }.

% Show plan length
plan_length(N) :- N = #count{ B, From, To, T : move(B, From, To, T) }.

% Show actions in order
action(move, B, From, To, T) :- move(B, From, To, T).

% Show final state for verification
final_on(X, P) :- on(X, P, 3).

% Show directives
#show plan_length/1.
#show action/5.
#show final_on/2.