% Ricochet Robots - Single-Step Movement Planning
% Grid 5x5, robots A, B, C, target for A at (2,3)
% Minimize number of moves

% --- Time Horizon ---
time(0..15).

% --- Grid Domain ---
row(0..4).
col(0..4).

% --- Robots ---
robot(a;b;c).

% --- Initial Positions (time 0) ---
at(a, 0, 1, 0).
at(b, 1, 1, 0).
at(c, 3, 1, 0).

% --- Walls ---
% Column 0 right side: rows 0-4 (blocked between col0 and col1)
wall_right(R, 0) :- row(R).
% Column 1 right side: rows 0-1 and 3-4 (blocked between col1 and col2 except row 2)
wall_right(R, 1) :- row(R), R != 2.
% Column 2 right side: rows 0-1 and 3-4 (blocked between col2 and col3 except row 2)
wall_right(R, 2) :- row(R), R != 2.

% --- Adjacency ---
adj(R, C, R-1, C) :- row(R), col(C), R > 0.   % up
adj(R, C, R+1, C) :- row(R), col(C), R < 4.   % down
adj(R, C, R, C-1) :- row(R), col(C), C > 0.   % left
adj(R, C, R, C+1) :- row(R), col(C), C < 4.   % right

% --- Blocked moves (by walls) ---
% right wall blocks movement right from (R, C) to (R, C+1)
blocked(R, C, R, C+1) :- wall_right(R, C), col(C), C+1 <= 4.
% right wall blocks movement left from (R, C+1) to (R, C)
blocked(R, C+1, R, C) :- wall_right(R, C), col(C), C+1 <= 4.

% --- Valid Move ---
valid_move(R1, C1, R2, C2) :- adj(R1, C1, R2, C2), not blocked(R1, C1, R2, C2).

% --- Finished: robot A reached target ---
finished(T) :- at(a, 2, 3, T).
finished(T+1) :- finished(T), time(T+1).

% --- Goal must be reached by end ---
:- not finished(max_time).

% --- Actions: exactly one robot moves per time step before finished ---
{ move(R, R2, C2, T) : robot(R), at(R, R1, C1, T), valid_move(R1, C1, R2, C2) } = 1 :-
    time(T), T < max_time, not finished(T).

% --- No moves after finished ---
:- move(_, _, _, T), finished(T).

% --- Effects: robot moves to new position ---
at(R, R2, C2, T+1) :- move(R, R2, C2, T).

% --- Frame: robots that don't move stay in place ---
at(R, R1, C1, T+1) :- at(R, R1, C1, T), time(T+1), not move(R, _, _, T).

% --- Collision constraint: no two robots in same cell at same time ---
:- at(R1, R, C, T), at(R2, R, C, T), R1 != R2.

% --- Move collision: cannot move into a cell occupied by another robot at current time ---
% move(Robot, RowTo, ColTo, Time) and at(OtherRobot, RowTo, ColTo, Time)
:- move(Robot, RowTo, ColTo, T), at(OtherRobot, RowTo, ColTo, T), Robot != OtherRobot.

% --- Minimize total moves ---
#minimize { 1, R, R2, C2, T : move(R, R2, C2, T) }.

% --- Output predicates ---
total_moves(N) :- N = #count { R, R2, C2, T : move(R, R2, C2, T) }.
final_pos(R, R1, C1) :- at(R, R1, C1, max_time).

#show total_moves/1.
#show final_pos/3.
#show move/4.