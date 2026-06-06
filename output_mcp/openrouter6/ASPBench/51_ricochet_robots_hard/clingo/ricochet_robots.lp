% Ricochet Robots puzzle - single-step movement variant

% Domain definitions
robot(a). robot(b). robot(c).
time(0..15).  % Horizon: enough for expected 7 moves

% Start positions
start_pos(a, 0, 1).
start_pos(b, 1, 1).
start_pos(c, 3, 1).

% Target position for robot a
target_pos(a, 2, 3).

% Walls: vertical barriers between columns
% wall_between(Row, Col) means there is a wall between Col and Col+1 at Row
wall_between(0,0). wall_between(1,0). wall_between(2,0). wall_between(3,0). wall_between(4,0).
wall_between(0,1). wall_between(1,1). wall_between(3,1). wall_between(4,1).
wall_between(0,2). wall_between(1,2). wall_between(3,2). wall_between(4,2).

% Grid bounds
row(0..4). col(0..4).

% Adjacent cells (Manhattan distance 1) - properly grounded
adjacent(R1,C1,R2,C2) :- row(R1), col(C1), row(R2), col(C2),
    R2 = R1+1, C2 = C1.
adjacent(R1,C1,R2,C2) :- row(R1), col(C1), row(R2), col(C2),
    R2 = R1-1, C2 = C1.
adjacent(R1,C1,R2,C2) :- row(R1), col(C1), row(R2), col(C2),
    R2 = R1, C2 = C1+1.
adjacent(R1,C1,R2,C2) :- row(R1), col(C1), row(R2), col(C2),
    R2 = R1, C2 = C1-1.

% Blocked by wall
blocked_wall(R1,C1,R2,C2) :- R1 = R2, C2 = C1+1, wall_between(R1, C1).
blocked_wall(R1,C1,R2,C2) :- R1 = R2, C2 = C1-1, wall_between(R1, C2).

% Occupied cell at time T
occupied(Row, Col, T) :- pos(_, Row, Col, T).

% Valid move conditions
valid_move(R, R1, C1, R2, C2, T) :-
    pos(R, R1, C1, T),
    adjacent(R1, C1, R2, C2),
    not blocked_wall(R1, C1, R2, C2),
    not occupied(R2, C2, T).

% Initial positions
pos(R, R1, C1, 0) :- start_pos(R, R1, C1).

% Move generation: exactly one move per time step
{ move(R, R1, C1, R2, C2, T) : valid_move(R, R1, C1, R2, C2, T) } 1 :- time(T), T < 15.

% Helper: robot R moved at time T
moved(R, T) :- move(R, _, _, _, _, T).

% State transition
% Robots that move
pos(R, R2, C2, T+1) :- move(R, R1, C1, R2, C2, T).
% Robots that don't move
pos(R, R1, C1, T+1) :- pos(R, R1, C1, T), not moved(R, T), time(T), T < 15.

% No two robots in same cell at same time
:- pos(R1, R, C, T), pos(R2, R, C, T), R1 != R2.

% Goal: robot a reaches target
goal_reached(T) :- pos(a, 2, 3, T).

% Minimize the time when goal is reached (i.e., number of moves)
#minimize { T : goal_reached(T) }.

% Output predicates
solution_found :- goal_reached(_).
moves(T) :- goal_reached(T).
sequence(T, R, R1, C1, R2, C2) :- move(R, R1, C1, R2, C2, T).
final_pos(R, R2, C2) :- pos(R, R2, C2, T), goal_reached(T).

% Show relevant atoms
#show solution_found/0.
#show moves/1.
#show sequence/6.
#show final_pos/3.