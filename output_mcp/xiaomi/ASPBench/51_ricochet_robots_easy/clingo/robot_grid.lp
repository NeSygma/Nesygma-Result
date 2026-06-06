% Grid puzzle: Robot A must reach target (2,1) with Robot B blocking

% === Domain Definitions ===
robot(a).
robot(b).

% Grid positions 0-3
row(0..3).
col(0..3).

% Time horizon - we need at most 10 moves
time(0..10).

% Directions
dir(north). dir(south). dir(east). dir(west).

% === Initial Positions ===
at(a, 0, 1, 0).
at(b, 1, 1, 0).

% === Target ===
target(a, 2, 1).

% === Walls ===
% Wall between column 1 and column 2 for rows 0 and 1 (vertical barrier on column 2 right side)
wall(0, 1, 0, 2).
wall(0, 2, 0, 1).
wall(1, 1, 1, 2).
wall(1, 2, 1, 1).

% === Adjacency Relations ===
% Moving north: (R,C) -> (R-1,C)
adjacent(R, C, R-1, C, north) :- row(R), col(C), R > 0.
% Moving south: (R,C) -> (R+1,C)
adjacent(R, C, R+1, C, south) :- row(R), col(C), R < 3.
% Moving west: (R,C) -> (R,C-1)
adjacent(R, C, R, C-1, west) :- row(R), col(C), C > 0.
% Moving east: (R,C) -> (R,C+1)
adjacent(R, C, R, C+1, east) :- row(R), col(C), C < 3.

% === Choice Rules ===
% At each time step, each robot can move in one direction or stay
{ move(R, D, T) : dir(D) } 1 :- robot(R), time(T), T > 0.

% === State Transitions ===
% Robot stays in place if no move
at(R, Row, Col, T) :- at(R, Row, Col, T-1), time(T), T > 0, not move(R, _, T-1).

% Robot moves to adjacent cell
at(R, NR, NC, T) :- move(R, D, T-1), at(R, OR, OC, T-1), adjacent(OR, OC, NR, NC, D), time(T), T > 0.

% === Constraints ===

% No wall crossing
:- move(R, D, T), at(R, OR, OC, T), adjacent(OR, OC, NR, NC, D), wall(OR, OC, NR, NC).

% No collisions - two robots cannot be at same position at same time
:- at(R1, Row, Col, T), at(R2, Row, Col, T), R1 != R2, time(T).

% Stay within grid bounds (already handled by adjacency, but explicit)
:- at(R, Row, Col, T), not row(Row).
:- at(R, Row, Col, T), not col(Col).

% === Goal Detection ===
goal_reached(T) :- at(a, 2, 1, T), time(T).

% Find earliest goal time
min_goal_time(T) :- goal_reached(T), T = #min{T2 : goal_reached(T2)}.

% === Solution Structure ===
solution_found :- min_goal_time(_).

% Count total moves up to goal time
total_moves(N) :- min_goal_time(G), N = #count{R,T : move(R, _, T), T < G}.

% === Move Sequence ===
% Assign order to moves
move_order(M, R, T) :- move(R, D, T), min_goal_time(G), T < G, 
                        M = #count{R2,T2 : move(R2, _, T2), T2 < T, min_goal_time(G)}.

% Record move details
move_seq(R, OR, OC, NR, NC, M) :- move(R, D, T), at(R, OR, OC, T), 
                                    adjacent(OR, OC, NR, NC, D), 
                                    move_order(M, R, T).

% === Final Positions ===
final_pos(R, Row, Col) :- min_goal_time(G), at(R, Row, Col, G).

% === Optimization ===
#minimize { G : min_goal_time(G) }.

% === Output ===
#show solution_found.
#show total_moves/1.
#show move_seq/6.
#show final_pos/3.