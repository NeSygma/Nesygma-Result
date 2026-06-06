% Grid and Robots
robot(a; b; c).
pos(0..4, 0..4).
#const max_moves=7.
time(0..max_moves).

start_pos(a, 0, 1).
start_pos(b, 1, 1).
start_pos(c, 3, 1).

% Walls (Vertical barriers)
% Column 0 right side: rows 0-4
blocked(R, 0, R, 1) :- R=0..4.
blocked(R, 1, R, 0) :- R=0..4.
% Column 1 right side: rows 0-1 and 3-4
blocked(R, 1, R, 2) :- R=0..1; R=3..4.
blocked(R, 2, R, 1) :- R=0..1; R=3..4.
% Column 2 right side: rows 0-1 and 3-4
blocked(R, 2, R, 3) :- R=0..1; R=3..4.
blocked(R, 3, R, 2) :- R=0..1; R=3..4.

% Initial State
at(Robot, R, C, 0) :- start_pos(Robot, R, C).

% Movement
{ move(Robot, R1, C1, R2, C2, T) : robot(Robot), pos(R1, C1), pos(R2, C2) } 1 :- time(T), T < max_moves.

% Preconditions
:- move(Robot, R1, C1, R2, C2, T), not at(Robot, R1, C1, T).
:- move(Robot, R1, C1, R2, C2, T), |R1-R2| + |C1-C2| != 1.
:- move(Robot, R1, C1, R2, C2, T), blocked(R1, C1, R2, C2).
:- move(Robot1, _, _, R, C, T), at(Robot2, R, C, T), Robot1 != Robot2.

% Effects
at(Robot, R2, C2, T+1) :- move(Robot, R1, C1, R2, C2, T).
at(Robot, R, C, T+1) :- at(Robot, R, C, T), not move(Robot, R, C, _, _, T), T < max_moves.

% Collision avoidance
:- at(Robot1, R, C, T), at(Robot2, R, C, T), Robot1 != Robot2.

% Goal
goal_reached(T) :- at(a, 2, 3, T).
:- not goal_reached(max_moves).

% Optimization
#minimize { T : goal_reached(T) }.

% Output
#show move/6.
#show at/4.
option(solution_found) :- goal_reached(max_moves).
#show option/1.