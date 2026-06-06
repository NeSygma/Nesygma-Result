% Ricochet Robots - Debug version with smaller horizon

% Grid 5x5, robots A, B, C, target for A at (2,3)
time(0..10).
row(0..4).
col(0..4).
robot(a;b;c).

% Initial positions
at(a, 0, 1, 0).
at(b, 1, 1, 0).
at(c, 3, 1, 0).

% Walls
wall_right(R, 0) :- row(R).
wall_right(R, 1) :- row(R), R != 2.
wall_right(R, 2) :- row(R), R != 2.

% Adjacency
adj(R, C, R-1, C) :- row(R), col(C), R > 0.
adj(R, C, R+1, C) :- row(R), col(C), R < 4.
adj(R, C, R, C-1) :- row(R), col(C), C > 0.
adj(R, C, R, C+1) :- row(R), col(C), C < 4.

% Blocked moves
blocked(R, C, R, C+1) :- wall_right(R, C), col(C), C+1 <= 4.
blocked(R, C+1, R, C) :- wall_right(R, C), col(C), C+1 <= 4.

% Valid move
valid_move(R1, C1, R2, C2) :- adj(R1, C1, R2, C2), not blocked(R1, C1, R2, C2).

% Finished
finished(T) :- at(a, 2, 3, T).
finished(T+1) :- finished(T), time(T+1).

% Exactly one move per step until finished
{ move(R, R2, C2, T) : robot(R), at(R, R1, C1, T), valid_move(R1, C1, R2, C2) } = 1 :-
    time(T), T < max_time, not finished(T).

% No moves after finished
:- move(_, _, _, T), finished(T).

% Effects
at(R, R2, C2, T+1) :- move(R, R2, C2, T).

% Frame
at(R, R1, C1, T+1) :- at(R, R1, C1, T), time(T+1), not move(R, _, _, T).

% No two robots in same cell
:- at(R1, R, C, T), at(R2, R, C, T), R1 != R2.

% Move collision
:- move(Robot, RowTo, ColTo, T), at(OtherRobot, RowTo, ColTo, T), Robot != OtherRobot.

% Must finish by end
:- not finished(max_time).

% Show results
#show move/4.
#show at/4.