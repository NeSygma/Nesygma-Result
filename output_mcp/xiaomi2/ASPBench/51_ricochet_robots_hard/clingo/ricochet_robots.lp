% Grid dimensions
row(0..4).
col(0..4).

% Robots
robot(a). robot(b). robot(c).

% Initial positions
init_pos(a, 0, 1).
init_pos(b, 1, 1).
init_pos(c, 3, 1).

% Target position for robot A
target(2, 3).

% Vertical walls: vwall(Row, Col) means wall on right side of column Col at row Row
% Blocks movement from (Row, Col) to (Row, Col+1)
vwall(R, 0) :- row(R).  % Column 0 right side: all rows 0-4
vwall(0, 1). vwall(1, 1). vwall(3, 1). vwall(4, 1).  % Column 1 right side: rows 0,1,3,4
vwall(0, 2). vwall(1, 2). vwall(3, 2). vwall(4, 2).  % Column 2 right side: rows 0,1,3,4

% Time horizon (expected minimum 7 moves)
max_t = 7.
time(0..max_t).

% Directions
dir(up). dir(down). dir(left). dir(right).

% Movement deltas
drow(up, -1). drow(down, 1). drow(left, 0). drow(right, 0).
dcol(up, 0). dcol(down, 0). dcol(left, -1). dcol(right, 1).

% Choice: at most one robot moves in one direction at each time step
{ move(R, D, T) : robot(R), dir(D) } 1 :- time(T), T > 0.

% State: pos(robot, row, col, time)
% Initial state
pos(R, Row, Col, 0) :- init_pos(R, Row, Col).

% Compute new position after move
new_pos(R, Row + DR, Col + DC, T) :- move(R, D, T), pos(R, Row, Col, T),
   drow(D, DR), dcol(D, DC).

% Validation: new position within grid bounds
:- new_pos(R, NR, _, _), NR < 0.
:- new_pos(R, NR, _, _), NR > 4.
:- new_pos(R, _, NC, _), NC < 0.
:- new_pos(R, _, NC, _), NC > 4.

% Validation: no wall blocking rightward move
:- move(R, right, T), pos(R, Row, Col, T), vwall(Row, Col).

% Validation: no wall blocking leftward move
:- move(R, left, T), pos(R, Row, Col, T), Col > 0, vwall(Row, Col - 1).

% Validation: cannot move to a cell occupied by another (stationary) robot
:- move(R1, _, T), pos(R2, NR, NC, T), R1 != R2, new_pos(R1, NR, NC, T).

% Frame axiom: position persists if robot does not move
moved(R, T) :- move(R, _, T).
pos(R, Row, Col, T+1) :- pos(R, Row, Col, T), time(T+1), not moved(R, T).

% Position update: robot moves to new position
pos(R, NR, NC, T+1) :- new_pos(R, NR, NC, T), time(T+1).

% Uniqueness: each robot has exactly one position at each time step
:- pos(R, R1, C1, T), pos(R, R2, C2, T), R1 != R2.
:- pos(R, R1, C1, T), pos(R, R2, C2, T), C1 != C2.

% Goal: robot a must reach target position (2, 3) at final time
:- not pos(a, 2, 3, max_t).

% Optimization: minimize total number of moves
#minimize { 1, R, D, T : move(R, D, T) }.

% Output predicates
solution_found.
#show solution_found.
#show move_seq/6.
move_seq(T, R, FromRow, FromCol, ToRow, ToCol) :- move(R, D, T),
   pos(R, FromRow, FromCol, T), new_pos(R, ToRow, ToCol, T).
#show final_pos/3.
final_pos(R, Row, Col) :- pos(R, Row, Col, max_t).
#show total_moves/1.
total_moves(N) :- N = #count { R, D, T : move(R, D, T) }.