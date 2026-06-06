% Grid Puzzle: Robot Coordination to Reach Target

% ===== DOMAIN DEFINITIONS =====
% Grid coordinates
row(0..3).
col(0..3).
position(R, C) :- row(R), col(C).

% Robots
robot("A").
robot("B").

% Time steps (we'll search for minimum moves)
time(0..10). % Sufficient horizon for optimal solution

% ===== STATIC FACTS =====
% Starting positions
start_pos("A", 0, 1).
start_pos("B", 1, 1).

% Target position for robot A
target_pos(2, 1).

% Walls (blocked cells)
wall(0, 2).
wall(1, 2).

% ===== DYNAMIC STATE =====
% Robot position at each time step
1 { pos(R, C, T) : position(C, R) } 1 :- robot(R), time(T).

% Initial positions
pos("A", 0, 1, 0).
pos("B", 1, 1, 0).

% ===== MOVEMENT RULES =====
% Define valid moves (cardinal directions)
% Move options: up, down, left, right
move(R, C, R, C+1, "right") :- position(R, C), position(R, C+1).
move(R, C, R, C-1, "left") :- position(R, C), position(R, C-1).
move(R, C, R+1, C, "down") :- position(R, C), position(R+1, C).
move(R, C, R-1, C, "up") :- position(R, C), position(R-1, C).

% ===== MOVEMENT GENERATION =====
% At each time step, exactly one robot moves exactly one step
% Choice rule: which robot moves and where
{ move_robot(R, FromR, FromC, ToR, ToC, T) } 1 :- 
    robot(R), time(T), T < 10,
    pos(R, FromR, FromC, T),
    move(FromR, FromC, ToR, ToC, _).

% ===== CONSTRAINTS =====
% 1. No moving through walls
:- move_robot(R, FromR, FromC, ToR, ToC, T), wall(ToR, ToC).

% 2. Stay within grid bounds (already enforced by position domain)

% 3. No collisions: robots cannot occupy same cell at same time
:- pos(R1, R, C, T), pos(R2, R, C, T), R1 != R2.

% 4. No moving into occupied cell (at same time step)
:- move_robot(R1, FromR1, FromC1, ToR, ToC, T),
   pos(R2, ToR, ToC, T), R1 != R2.

% 5. Robots must move to adjacent cells (already enforced by move/5)

% ===== STATE TRANSITIONS =====
% Frame axiom: position persists if robot doesn't move
pos(R, R, C, T+1) :- pos(R, R, C, T), time(T), time(T+1),
    not move_robot(R, R, C, _, _, T).

% Effect: position changes when robot moves
pos(R, ToR, ToC, T+1) :- move_robot(R, FromR, FromC, ToR, ToC, T),
    time(T), time(T+1).

% ===== GOAL CONDITION =====
% Robot A must be at target position
goal(T) :- pos("A", 2, 1, T).

% ===== OPTIMIZATION =====
% Minimize number of moves (time steps until goal)
#minimize { 1,T : goal(T) }.

% ===== OUTPUT =====
% Show solution
#show solution_found/0.
#show moves/1.
#show sequence/6.
#show final_positions/4.

% Helper for output
solution_found :- goal(T), time(T).
moves(T) :- goal(T), time(T).

% Sequence output (robot, from_row, from_col, to_row, to_col, time)
sequence(R, FromR, FromC, ToR, ToC, T) :- 
    move_robot(R, FromR, FromC, ToR, ToC, T).

% Final positions
final_pos(R, R, C) :- pos(R, R, C, T), goal(T).

% Show key information
#show solution_found.
#show moves(T) : goal(T).
#show sequence(R, FromR, FromC, ToR, ToC, T) : move_robot(R, FromR, FromC, ToR, ToC, T).
#show final_pos(R, R, C) : pos(R, R, C, T), goal(T).