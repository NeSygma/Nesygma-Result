% Domains
time(0..4). % Time horizon (can be increased if needed)
robot(a; b).
row(0..3).
col(0..3).

% Walls: vertical walls at column 2, rows 0-1
% These walls block movement between (Row,1) and (Row,2) for Row in {0,1}
% Represented as wall(Row, FromCol, ToCol)
wall(0, 1, 2).
wall(1, 1, 2).

% Initial positions
at(a, 0, 1, 0).
at(b, 1, 1, 0).

% Target position
target(2, 1).

% Valid moves: single-step cardinal moves, no wall crossing, within bounds
valid_move(R, FR, FC, TR, TC, T) :-
    robot(R),
    time(T),
    at(R, FR, FC, T),
    % Single-step cardinal move
    ( (FR - TR = 1, FC = FC) ;
      (TR - FR = 1, FC = FC) ;
      (FC - TC = 1, FR = FR) ;
      (TC - FC = 1, FR = FR) ),
    0 <= TR, TR <= 3,
    0 <= TC, TC <= 3,
    not wall(TR, min(FC, TC), max(FC, TC)). % Check if the move crosses a wall

% Choice rule: robots can move or stay (staying is modeled as not moving)
{ move(R, FR, FC, TR, TC, T) : valid_move(R, FR, FC, TR, TC, T) } 1 :-
    robot(R),
    time(T),
    at(R, FR, FC, T).

% Update positions based on moves
at(R, TR, TC, T+1) :- move(R, _, _, TR, TC, T), time(T), time(T+1).

% No collisions: no two robots at the same position at the same time
:- time(T), robot(R1), robot(R2), R1 != R2,
   at(R1, R, C, T), at(R2, R, C, T).

% Goal: Robot A must be at the target position at the final time step
:- time(T), target(R, C), not at(a, R, C, T).

% Count the number of moves
move_count(N) :-
    N = #count{ move(R, _, _, _, _, T) : robot(R), time(T) }.

% Final positions
final_positions(R, R, C) :- at(R, R, C, T), time(T), not move(R, _, _, _, _, T).

% Solution found if Robot A is at the target at the final time step
solution_found :- time(T), at(a, 2, 1, T).

% Minimize the number of moves
#minimize{ 1@1, M : move_count(M) }.

% Show the required outputs
#show solution_found/0.
#show move_count/1.
#show move/6.
#show final_positions/3.