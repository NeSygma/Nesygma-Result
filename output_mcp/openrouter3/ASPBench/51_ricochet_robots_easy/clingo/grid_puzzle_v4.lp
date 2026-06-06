% Grid Puzzle: Robot Coordination to Reach Target

% ===== DOMAIN DEFINITIONS =====
% Grid coordinates
row(0..3).
col(0..3).
position(R, C) :- row(R), col(C).

% Robots
robot("A").
robot("B").

% Time steps
time(0..10).

% ===== STATIC FACTS =====
% Starting positions
start_pos("A", 0, 1).
start_pos("B", 1, 1).

% Target position for robot A
target_pos(2, 1).

% Walls (blocked cells) - vertical barrier at column 2, rows 0-1
wall(0, 2).
wall(1, 2).

% ===== DYNAMIC STATE =====
% Robot position at each time step
% Exactly one position per robot per time
1 { pos(R, R, C) : position(R, C) } 1 :- robot(R), time(T).

% Initial positions
pos("A", 0, 1) :- time(0).
pos("B", 1, 1) :- time(0).

% ===== MOVEMENT GENERATION =====
% At each time step, exactly one robot moves exactly one step
% Define possible moves
move_dir(0, 1).  % right
move_dir(0, -1). % left
move_dir(1, 0).  % down
move_dir(-1, 0). % up

% Choice rule for which robot moves and where
{ move(R, FromR, FromC, ToR, ToC, T) } 1 :- 
    robot(R), time(T), T < 10,
    pos(R, FromR, FromC, T),
    ToR = FromR + DR, ToC = FromC + DC,
    move_dir(DR, DC),
    position(ToR, ToC).

% ===== CONSTRAINTS =====
% 1. No moving through walls
:- move(R, FromR, FromC, ToR, ToC, T), wall(ToR, ToC).

% 2. No collisions: robots cannot occupy same cell at same time
:- pos(R1, R, C, T), pos(R2, R, C, T), R1 != R2.

% 3. No moving into occupied cell
:- move(R1, FromR1, FromC1, ToR, ToC, T),
   pos(R2, ToR, ToC, T), R1 != R2.

% ===== STATE TRANSITIONS =====
% Frame axiom: position persists if robot doesn't move
pos(R, R, C, T+1) :- pos(R, R, C, T), time(T), time(T+1),
    not move(R, R, C, _, _, T).

% Effect: position changes when robot moves
pos(R, ToR, ToC, T+1) :- move(R, FromR, FromC, ToR, ToC, T),
    time(T), time(T+1).

% ===== GOAL CONDITION =====
% Robot A must be at target position
goal(T) :- pos("A", 2, 1, T).

% ===== OPTIMIZATION =====
% Minimize number of moves (time steps until goal)
#minimize { 1,T : goal(T) }.

% ===== OUTPUT =====
% Helper for output
solution_found :- goal(T), time(T).
moves(T) :- goal(T), time(T).

% Sequence output
sequence(R, FromR, FromC, ToR, ToC, T) :- 
    move(R, FromR, FromC, ToR, ToC, T).

% Final positions
final_pos(R, R, C) :- pos(R, R, C, T) :- goal(T).

% Show key information
#show solution_found/0.
#show moves/1.
#show sequence/6.
#show final_positions/4.