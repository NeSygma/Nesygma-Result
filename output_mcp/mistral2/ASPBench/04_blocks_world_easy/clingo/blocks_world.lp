% Define the blocks and the table
block(a). block(b). block(c).
table(table).

% Define the initial and goal states
% Initial state:
% - Block A is on the table
% - Block B is on the table
% - Block C is on top of block A
on(c, a, 0).
on(a, table, 0).
on(b, table, 0).

% Goal state:
% - Block A is on top of block B
% - Block B is on top of block C
% - Block C is on the table
on(a, b, final).
on(b, c, final).
on(c, table, final).

% Time horizon: 0 to max_time (we will search for the minimal plan length)
% We set a reasonable upper bound for the plan length (e.g., 10 steps)
time(0..10).

% A block is clear if nothing is on top of it
clear(X, T) :- block(X), time(T), not on(_, X, T).

% A block can be moved if it is clear
can_move(X, T) :- block(X), time(T), clear(X, T).

% Only one block can be moved per time step
1 { move(X, From, To, T) : block(X), can_move(X, T), table(From), table(To), From != To } 1 :- time(T).

% Frame axioms: if a block is not moved, its position remains the same
on(X, Y, T+1) :- on(X, Y, T), time(T), time(T+1), not moved(X, T).

% If a block is moved, its new position is updated
on(X, To, T+1) :- move(X, _, To, T), time(T), time(T+1).

% The source position must be correct at time T
:- move(X, From, _, T), time(T), not on(X, From, T).

% The target position must be valid (either table or another block)
:- move(X, _, To, T), time(T), block(To), not clear(To, T).

% No block can be placed on itself
:- move(X, _, X, T), time(T).

% At most one block can be on top of another block (except the table)
:- on(X, Y, T), on(Z, Y, T), X != Z, block(Y), time(T).

% Define moved/2 to track which blocks are moved at each time step
moved(X, T) :- move(X, _, _, T), time(T).

% The plan must end at the goal state
:- not goal_reached(T), time(T).
goal_reached(T) :- on(a, b, T), on(b, c, T), on(c, table, T), time(T).

% Minimize the number of moves
#minimize { T@1 : time(T), goal_reached(T) }.

% Show the plan
#show move/4.
#show plan_length/1.
plan_length(N) :- N = #count { T : goal_reached(T) }, time(T).