%% Domains and initial data
block(a; b; c; d; e; f; g; h; i; j; k; l).
weight(a,1). weight(b,2). weight(c,3). weight(d,4). weight(e,5). weight(f,6). weight(g,7). weight(h,8). weight(i,9). weight(j,10). weight(k,11). weight(l,12).

max_time(50).
time(0..T) :- max_time(T).

% Initial configuration (time 0)
on(d, table, 0). on(c, d, 0). on(b, c, 0). on(a, b, 0).
on(h, table, 0). on(g, h, 0). on(f, g, 0). on(e, f, 0).
on(l, table, 0). on(k, l, 0). on(j, k, 0). on(i, j, 0).

% Goal configuration (time max_time)
% Define the goal as a set of constraints
goal_on(l, table, T) :- max_time(T).
goal_on(i, l, T) :- max_time(T).
goal_on(f, i, T) :- max_time(T).
goal_on(c, f, T) :- max_time(T).
goal_on(k, table, T) :- max_time(T).
goal_on(h, k, T) :- max_time(T).
goal_on(e, h, T) :- max_time(T).
goal_on(b, e, T) :- max_time(T).
goal_on(j, table, T) :- max_time(T).
goal_on(g, j, T) :- max_time(T).
goal_on(d, g, T) :- max_time(T).
goal_on(a, d, T) :- max_time(T).

% Helper: block X is clear at time T if nothing is on X at T
clear(X, T) :- block(X), time(T), not on(_, X, T).

% Helper: count blocks directly on the table at time T
table_count(C, T) :- C = #count { X : on(X, table, T) }, time(T).

% Helper: height of the tower rooted at X at time T
tower_root(X, T) :- on(X, table, T), time(T).
tower_root(X, T) :- on(X, Y, T), time(T), not on(_, X, T).

height(X, 1, T) :- tower_root(X, T), time(T).
height(X, H+1, T) :- on(Y, X, T), time(T), height(X, H, T), H < 5.

% Choice rule: at most one move per time step (except last)
{ move(Block, From, To, Time) : block(Block), from_pos(From, Time), to_pos(To, Time) } 1 :- time(Time), Time < max_time.

% Define valid from_pos and to_pos
from_pos(Pos, Time) :- on(Block, Pos, Time), clear(Block, Time), time(Time).
from_pos(table, Time) :- time(Time). % Allow moving from table (if a block is on table and clear)

to_pos(table, Time) :- time(Time).
to_pos(Pos, Time) :- clear(Pos, Time), time(Time).

% Preconditions for move(Block, From, To, Time):
% 1. Block must be clear
% 2. From must be the current position of Block
% 3. To must be a valid position
:- move(Block, From, To, Time), not clear(Block, Time).
:- move(Block, From, To, Time), not on(Block, From, Time).
:- move(Block, From, To, Time), not to_pos(To, Time).
:- move(Block, From, To, Time), From == To.

% Weight constraint: if To is a block, weight(To) >= weight(Block)
:- move(Block, From, To, Time), block(To), weight(To, W1), weight(Block, W2), W1 < W2.

% Table limit: after move, table_count <= 6
:- move(Block, From, To, Time), table_count(C, Time+1), C > 6.

% Height limit: after move, no tower exceeds height 5
:- move(Block, From, To, Time), height(To, H, Time+1), H > 5.
:- move(Block, From, table, To, Time), height(To, H, Time+1), H > 5.

% Effects of move(Block, From, To, Time):
on(Block, To, Time+1) :- move(Block, From, To, Time), time(Time).

% If From is a block, it becomes clear (unless something is moved onto it later in the same step)
on(Other, From, Time+1) :- on(Other, From, Time), not move(Other, From, _, Time), time(Time).

% If To is a block, it is no longer clear (since Block is now on it)
:- move(Block, From, To, Time), block(To), clear(To, Time+1).

% Persistence for other blocks not involved in the move
on(Block, Pos, Time+1) :- on(Block, Pos, Time), not move(Block, _, _, Time), time(Time).

% Ensure clear/2 is updated correctly
clear(X, Time+1) :- block(X), time(Time+1), not on(_, X, Time+1).

% Update table_count and height after move (via helper predicates)

% Goal satisfaction at max_time
:- goal_on(X, Y, T), not on(X, Y, T), max_time(T).

% Show the plan
#show move/4.

% Optional: show the final state for debugging
#show on/3.