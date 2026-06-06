% === Ricochet Robots - Single Step Movement ===
% Find minimum moves for Robot A to reach target (2,3)

% Grid dimensions
row(0..4).
col(0..4).

% Positions
pos(R, C) :- row(R), col(C).

% Robots
robot(a). robot(b). robot(c).

% Starting positions
start(a, 0, 1).
start(b, 1, 1).
start(c, 3, 1).

% Target for Robot A
target(2, 3).

% === Wall Definitions ===
% Wall between (R,C1) and (R,C2) where C2 = C1+1 (vertical wall on right side of C1)
% Column 0 right side: rows 0-4
wall(R, 0, R, 1) :- row(R), R <= 4.

% Column 1 right side: rows 0-1 and 3-4
wall(R, 1, R, 2) :- row(R), R <= 1.
wall(R, 1, R, 2) :- row(R), R >= 3, R <= 4.

% Column 2 right side: rows 0-1 and 3-4
wall(R, 2, R, 3) :- row(R), R <= 1.
wall(R, 2, R, 3) :- row(R), R >= 3, R <= 4.

% Walls are symmetric
wall(R2, C2, R1, C1) :- wall(R1, C1, R2, C2).

% === Adjacency ===
% Two cells are adjacent if they differ by 1 in exactly one coordinate
% and there is no wall between them
adjacent(R1, C1, R2, C2) :- pos(R1, C1), pos(R2, C2), 
    R2 = R1 + 1, C2 = C1, not wall(R1, C1, R2, C2).
adjacent(R1, C1, R2, C2) :- pos(R1, C1), pos(R2, C2), 
    R2 = R1 - 1, C2 = C1, not wall(R1, C1, R2, C2).
adjacent(R1, C1, R2, C2) :- pos(R1, C1), pos(R2, C2), 
    R2 = R1, C2 = C1 + 1, not wall(R1, C1, R2, C2).
adjacent(R1, C1, R2, C2) :- pos(R1, C1), pos(R2, C2), 
    R2 = R1, C2 = C1 - 1, not wall(R1, C1, R2, C2).

% === Time Horizon ===
% We need at most 10 moves (generous bound)
time(0..10).

% === Initial State ===
at(R, Rr, Rc, 0) :- start(R, Rr, Rc).

% === Move Actions ===
% At each time step, exactly one robot makes one move to an adjacent cell
1 { move(R, Rr1, Rc1, Rr2, Rc2, T) : robot(R), 
    pos(Rr1, Rc1), pos(Rr2, Rc2), adjacent(Rr1, Rc1, Rr2, Rc2) } 1 :- time(T), T > 0.

% A move must start from the robot's current position
:- move(R, Rr1, Rc1, Rr2, Rc2, T), not at(R, Rr1, Rc1, T-1).

% === State Update ===
% Robot moves to new position
at(R, Rr2, Rc2, T) :- move(R, Rr1, Rc1, Rr2, Rc2, T).

% Other robots stay in place (frame axiom)
at(R, Rr, Rc, T) :- at(R, Rr, Rc, T-1), time(T), T > 0,
    not move(R, _, _, _, _, T).

% === Constraints ===
% No two robots can occupy the same cell at the same time
:- at(R1, Rr, Rc, T), at(R2, Rr, Rc, T), R1 != R2, time(T).

% === Goal ===
% Robot A must reach the target
goal_reached(T) :- at(a, 2, 3, T), time(T).

% Find the earliest time the goal is reached
min_goal_time(M) :- M = #min { T : goal_reached(T) }.

% Only keep states up to the goal time
:- at(_, _, _, T), min_goal_time(M), T > M.

% === Optimization ===
#minimize { 1, T : move(_, _, _, _, _, T) }.

% === Output ===
#show move/6.
#show at/4.
#show min_goal_time/1.
#show solution_found/0.

solution_found :- min_goal_time(_).