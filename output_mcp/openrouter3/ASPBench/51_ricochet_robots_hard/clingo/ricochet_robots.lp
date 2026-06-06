% Ricochet Robots Puzzle - Single-step movement variant

% ===== DOMAIN DEFINITIONS =====
% Grid coordinates
row(0..4).
col(0..4).
position(R, C) :- row(R), col(C).

% Robots
robot("A").
robot("B").
robot("C").

% Time steps (0 = initial state, 1..N = after N moves)
time(0..20). % Sufficient for 7 moves

% ===== INITIAL POSITIONS =====
initial_position("A", 0, 1).
initial_position("B", 1, 1).
initial_position("C", 3, 1).

% Target position for robot A
target_position(2, 3).

% ===== WALL DEFINITIONS =====
% Walls are vertical barriers between columns
% wall_right(C, R) means there's a wall on the right side of column C at row R
% This prevents movement from (R, C) to (R, C+1)

% Left boundary (column 0 right side)
wall_right(0, 0). wall_right(0, 1). wall_right(0, 2). wall_right(0, 3). wall_right(0, 4).

% Column 1 right side (creates bridge opening at row 2)
wall_right(1, 0). wall_right(1, 1). 
% No wall at row 2 (bridge opening)
wall_right(1, 3). wall_right(1, 4).

% Column 2 right side (creates bridge opening at row 2)
wall_right(2, 0). wall_right(2, 1).
% No wall at row 2 (bridge opening)
wall_right(2, 3). wall_right(2, 4).

% ===== MOVEMENT RULES =====
% Position of each robot at each time step
{ position(Robot, R, C, T) } :- robot(Robot), position(R, C), time(T).

% Initial positions
position(Robot, R, C, 0) :- initial_position(Robot, R, C).

% Single-step movement: exactly one cell in cardinal direction
% Movement from (R, C) to (R+1, C) - down
move_down(Robot, R, C, T) :- 
    position(Robot, R, C, T), 
    position(Robot, R+1, C, T+1),
    row(R+1), not wall_down(R, C).

% Movement from (R, C) to (R-1, C) - up
move_up(Robot, R, C, T) :- 
    position(Robot, R, C, T), 
    position(Robot, R-1, C, T+1),
    row(R-1), not wall_up(R, C).

% Movement from (R, C) to (R, C+1) - right
move_right(Robot, R, C, T) :- 
    position(Robot, R, C, T), 
    position(Robot, R, C+1, T+1),
    col(C+1), not wall_right(C, R).

% Movement from (R, C) to (R, C-1) - left
move_left(Robot, R, C, T) :- 
    position(Robot, R, C, T), 
    position(Robot, R, C-1, T+1),
    col(C-1), not wall_right(C-1, R).

% Define wall constraints for up/down movements
% (For simplicity, we'll assume no horizontal walls in this problem)
wall_up(R, C) :- false. % No horizontal walls defined
wall_down(R, C) :- false. % No horizontal walls defined

% ===== CONSTRAINTS =====
% 1. No collisions: Multiple robots cannot occupy same cell at same time
:- position(R1, R, C, T), position(R2, R, C, T), R1 != R2, time(T).

% 2. Robots must stay within grid bounds
:- position(Robot, R, C, T), not position(Robot, R, C, T), time(T), 
   (R < 0; R > 4; C < 0; C > 4).

% 3. Exactly one move per time step (except initial state)
% At each time step T > 0, exactly one robot moves
% We'll count moves and ensure sequential execution

% ===== MOVEMENT TRACKING =====
% Track which robot moves at each time step
{ moved(Robot, T) } :- robot(Robot), time(T), T > 0.

% Each time step has exactly one robot moving
1 { moved(Robot, T) : robot(Robot) } 1 :- time(T), T > 0.

% If a robot moves at time T, its position changes
position(Robot, R_new, C_new, T+1) :- 
    moved(Robot, T),
    position(Robot, R_old, C_old, T),
    (move_down(Robot, R_old, C_old, T); 
     move_up(Robot, R_old, C_old, T);
     move_right(Robot, R_old, C_old, T);
     move_left(Robot, R_old, C_old, T)),
    position(Robot, R_new, C_new, T+1).

% Frame axiom: If a robot doesn't move, its position persists
position(Robot, R, C, T+1) :- 
    position(Robot, R, C, T),
    not moved(Robot, T),
    time(T).

% ===== GOAL CONDITION =====
% Robot A must reach target position (2, 3)
goal_reached :- position("A", 2, 3, T), time(T).

% ===== OPTIMIZATION =====
% Minimize total number of moves
#minimize { 1,T : moved(_, T) }.

% ===== OUTPUT =====
% Show solution information
solution_found :- goal_reached.
moves(N) :- N = #count { T : moved(_, T) }.

% Final positions
final_position(Robot, R, C) :- position(Robot, R, C, T), 
                                not position(Robot, R, C, T+1), 
                                time(T), time(T+1).

% Show key information
#show solution_found/0.
#show moves/1.
#show final_position/3.
#show position/4.
#show moved/2.