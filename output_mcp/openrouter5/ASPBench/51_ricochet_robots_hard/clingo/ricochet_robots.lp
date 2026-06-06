%% Ricochet Robots - Single Step Movement
%% Grid: 5x5, coordinates 0-4

%% ========== DOMAINS ==========
robot(a; b; c).
row(0..4).
col(0..4).
time(0..7).  %% Expected minimum is 7 moves, so we search up to 7

%% ========== WALL DEFINITIONS ==========
%% Walls are vertical barriers between (row, col) and (row, col+1)
%% wall_at(Row, Col) means there is a wall on the right side of cell (Row, Col)
wall_at(R, 0) :- row(R).  %% Column 0 right side: rows 0-4
wall_at(R, 1) :- row(R), R != 2.  %% Column 1 right side: rows 0-1 and 3-4
wall_at(R, 2) :- row(R), R != 2.  %% Column 2 right side: rows 0-1 and 3-4

%% ========== INITIAL POSITIONS ==========
pos(a, 0, 1, 0).  %% Robot A starts at (0,1) at time 0
pos(b, 1, 1, 0).  %% Robot B starts at (1,1) at time 0
pos(c, 3, 1, 0).  %% Robot C starts at (3,1) at time 0

%% ========== MOVEMENT GENERATION ==========
%% At each time step, exactly one robot moves to an adjacent cell
{ move(R, R1, C1, T) : robot(R), row(R1), col(C1) } 1 :- time(T), T < 7.

%% ========== MOVEMENT VALIDITY ==========
%% A move must be from the robot's current position
:- move(R, R1, C1, T), not pos(R, R1, C1, T).

%% A move must be exactly one step in a cardinal direction
%% The destination must be adjacent (Manhattan distance = 1)
:- move(R, R1, C1, T), pos(R, R0, C0, T), |R1 - R0| + |C1 - C0| != 1.

%% ========== WALL CONSTRAINTS ==========
%% Cannot move right if there's a wall on the right side of current cell
:- move(R, R1, C1, T), pos(R, R0, C0, T), C1 = C0 + 1, wall_at(R0, C0).

%% Cannot move left if there's a wall on the right side of the destination cell
:- move(R, R1, C1, T), pos(R, R0, C0, T), C1 = C0 - 1, wall_at(R1, C1).

%% ========== COLLISION CONSTRAINTS ==========
%% Two robots cannot occupy the same cell at the same time
:- pos(R1, Row, Col, T), pos(R2, Row, Col, T), R1 != R2.

%% ========== EFFECTS (STATE UPDATE) ==========
%% If a robot moves, it arrives at the destination
pos(R, R1, C1, T+1) :- move(R, R1, C1, T), time(T+1).

%% If a robot does not move, it stays in place (frame axiom)
pos(R, R0, C0, T+1) :- pos(R, R0, C0, T), time(T+1), not move(R, R0, C0, T).

%% ========== GOAL ==========
%% Robot A must reach target (2,3) at some time
goal_reached(T) :- pos(a, 2, 3, T).
:- not goal_reached(T), time(T).  %% Must reach goal by the final time

%% ========== OPTIMIZATION ==========
%% Minimize the time when the goal is first reached
#minimize { T@1 : goal_reached(T) }.

%% ========== OUTPUT ==========
solution_found :- goal_reached(T).

%% Extract the move sequence
moves(T) :- goal_reached(T).

%% Show move details
#show solution_found/0.
#show moves/1.
#show move/4.
#show pos/4.