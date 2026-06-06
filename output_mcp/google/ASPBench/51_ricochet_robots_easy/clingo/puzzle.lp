% Grid and Constants
#const max_moves = 6.
time(0..max_moves).
row(0..3). col(0..3).
robot(a; b).

% Initial Positions
at(a, 0, 1, 0).
at(b, 1, 1, 0).

% Target
target(a, 2, 1).

% Walls: Wall between (0,1) and (0,2), and (1,1) and (1,2)
% Represented as blocked movement between adjacent cells
blocked(0, 1, 0, 2).
blocked(0, 2, 0, 1).
blocked(1, 1, 1, 2).
blocked(1, 2, 1, 1).

% Movement
{ move(Robot, R1, C1, R2, C2, T) : 
    row(R1), col(C1), row(R2), col(C2), 
    |R1-R2| + |C1-C2| == 1, 
    not blocked(R1, C1, R2, C2) 
} 1 :- robot(Robot), time(T), T < max_moves.

% Preconditions
:- move(Robot, R1, C1, R2, C2, T), not at(Robot, R1, C1, T).
:- move(Robot, _, _, R2, C2, T), at(Other, R2, C2, T), Robot != Other.
:- move(Robot, _, _, R2, C2, T), not row(R2).
:- move(Robot, _, _, R2, C2, T), not col(C2).

% Effects
at(Robot, R2, C2, T+1) :- move(Robot, R1, C1, R2, C2, T).
at(Robot, R, C, T+1) :- at(Robot, R, C, T), not moved(Robot, T), time(T), T < max_moves.
moved(Robot, T) :- move(Robot, _, _, _, _, T).

% Collision avoidance at T+1
:- at(R1, Row, Col, T), at(R2, Row, Col, T), R1 != R2, time(T).

% Goal
goal_reached(T) :- at(a, 2, 1, T).
:- not goal_reached(max_moves).

% Optimization
#minimize { 1, T : move(_, _, _, _, _, T) }.

% Output
#show move/6.
#show at/4.
#show goal_reached/1.