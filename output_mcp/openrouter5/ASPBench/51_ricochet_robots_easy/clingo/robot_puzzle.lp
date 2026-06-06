%% Problem: Robot A must reach (2,1) with help from Robot B
%% Grid: 4x4 (rows/cols 0-3)
%% Robot A starts at (0,1), Robot B starts at (1,1)
%% Walls: column 2 right side, rows 0-1

%% Domain definitions
row(0..3).
col(0..3).
robot(a;b).

%% Starting positions
start(a, 0, 1).
start(b, 1, 1).

%% Target for robot A
target(a, 2, 1).

%% Wall: between (r,2) and (r,3) for r=0,1
wall(0, 2, 3).
wall(1, 2, 3).

%% Adjacent cells (Manhattan distance = 1, within bounds)
adj(R1, C1, R2, C2) :- row(R1), col(C1), row(R2), col(C2), |R1-R2| + |C1-C2| = 1.

%% Blocked moves due to walls
blocked(R, C1, C2) :- wall(R, C1, C2).
blocked(R, C2, C1) :- wall(R, C1, C2).

%% Time horizon - we expect 3 moves minimum, allow up to 6
time(0..6).

%% Position of each robot at each time
%% At time 0, robots are at start positions
pos(a, R, C, 0) :- start(a, R, C).
pos(b, R, C, 0) :- start(b, R, C).

%% Each robot can move at most once per time step
{move(R, R1, C1, R2, C2, T) : adj(R1, C1, R2, C2), not blocked(R1, C1, R2, C2)} 1 :- robot(R), time(T), T < 6, pos(R, R1, C1, T).

%% Exactly one move per time step (sequential execution)
:- time(T), T < 6, #count{R : move(R, _, _, _, _, T)} != 1.

%% A robot can only move if it's at the from position
:- move(R, R1, C1, _, _, T), not pos(R, R1, C1, T).

%% No collisions: two robots cannot occupy same cell at same time
:- pos(R1, R, C, T), pos(R2, R, C, T), R1 != R2.

%% A robot cannot move to a cell occupied by another robot at the same time
:- move(R, _, _, R2, C2, T), pos(R_other, R2, C2, T), R != R_other.

%% Effect: if robot moves, it's at the new position at T+1
pos(R, R2, C2, T+1) :- move(R, _, _, R2, C2, T), time(T+1).

%% Frame axiom: if robot doesn't move, it stays in place
pos(R, R1, C1, T+1) :- pos(R, R1, C1, T), time(T+1), not move(R, R1, C1, _, _, T).

%% Each robot has exactly one position at each time
:- pos(R, R1, C1, T), pos(R, R2, C2, T), R1 != R2.
:- pos(R, R1, C1, T), pos(R, R1, C2, T), C1 != C2.

%% Goal: Robot A reaches target at some time
goal_reached(T) :- pos(a, R, C, T), target(a, R, C).

%% Must reach goal by the end
:- not goal_reached(T) : time(T).

%% Minimize the number of moves
total_moves(N) :- N = #count{R, T : move(R, _, _, _, _, T)}.

#minimize { N : total_moves(N) }.

%% Output
#show pos/4.
#show move/6.
#show total_moves/1.
#show goal_reached/1.