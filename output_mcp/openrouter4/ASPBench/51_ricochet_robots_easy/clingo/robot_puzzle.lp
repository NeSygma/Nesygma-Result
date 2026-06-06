% --- Constants and Domain ---
#const max_time = 6.

robot("A").
robot("B").

time(0..max_time).

direction(1,0).
direction(-1,0).
direction(0,1).
direction(0,-1).

% --- Grid and Walls ---
wall(0,2).
wall(1,2).

% --- Initial Positions ---
robot_pos("A", 0, 1, 0).
robot_pos("B", 1, 1, 0).

% --- Move Choices: at each time step, at most one robot moves one step ---
0 { move(R, DR, DC, T) : robot(R), direction(DR, DC) } 1 :- time(T), T < max_time.

% --- Helper: which robot moves at time T ---
moves_robot(R, T) :- move(R, _, _, T).

% --- Effects: update position for moving robot ---
robot_pos(R, ROW_NEW, COL_NEW, T+1) :- 
    move(R, DR, DC, T), 
    robot_pos(R, ROW, COL, T), 
    ROW_NEW = ROW + DR, 
    COL_NEW = COL + DC,
    time(T), T < max_time.

% --- Frame: position persists for robots that do not move ---
robot_pos(R, ROW, COL, T+1) :- 
    robot_pos(R, ROW, COL, T), 
    time(T), T < max_time, 
    not moves_robot(R, T).

% --- Constraints ---

% 1. Stay within grid bounds (split into separate constraints)
:- move(R, DR, DC, T), robot_pos(R, ROW, COL, T), ROW + DR < 0.
:- move(R, DR, DC, T), robot_pos(R, ROW, COL, T), ROW + DR > 3.
:- move(R, DR, DC, T), robot_pos(R, ROW, COL, T), COL + DC < 0.
:- move(R, DR, DC, T), robot_pos(R, ROW, COL, T), COL + DC > 3.

% 2. Cannot move into a wall cell
:- move(R, DR, DC, T), robot_pos(R, ROW, COL, T),
   wall(ROW + DR, COL + DC).

% 3. Cannot occupy a wall cell at any time
:- robot_pos(R, ROW, COL, T), wall(ROW, COL).

% 4. No collisions: two robots cannot occupy the same cell at the same time
:- robot_pos(R1, ROW, COL, T), robot_pos(R2, ROW, COL, T), R1 != R2.

% 5. Cannot move into a cell occupied by another robot at the same time
:- move(R, DR, DC, T), robot_pos(R, ROW, COL, T),
   robot_pos(R2, ROW + DR, COL + DC, T), R != R2.

% 6. Goal must be achieved by final time
:- not robot_pos("A", 2, 1, max_time).

% --- Derived Output Predicates ---

% Solution found indicator
solution_found :- robot_pos("A", 2, 1, max_time).

% Total number of moves
total_moves(N) :- N = #count { T, R, DR, DC : move(R, DR, DC, T) }.

% Move atoms with full from/to positions for sequence output
move_at(R, FROM_ROW, FROM_COL, TO_ROW, TO_COL, T) :-
    move(R, DR, DC, T),
    robot_pos(R, FROM_ROW, FROM_COL, T),
    TO_ROW = FROM_ROW + DR,
    TO_COL = FROM_COL + DC.

% Final positions of all robots
final_pos(R, ROW, COL) :- robot_pos(R, ROW, COL, max_time).

% --- Minimize total number of moves ---
#minimize { 1, R, DR, DC, T : move(R, DR, DC, T) }.

% --- Show Directives ---
#show solution_found/0.
#show total_moves/1.
#show move_at/6.
#show final_pos/3.