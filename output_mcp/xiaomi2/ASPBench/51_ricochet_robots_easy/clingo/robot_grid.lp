% Grid dimensions
row(0..3).
col(0..3).

% Robots
robot(a).
robot(b).

% Starting positions
start(a, 0, 1).
start(b, 1, 1).

% Target for robot A
target(a, 2, 1).

% Walls - block movement between adjacent cells
% Wall on right side of column 2, rows 0-1
wall(0, 2, 0, 3).
wall(0, 3, 0, 2).
wall(1, 2, 1, 3).
wall(1, 3, 1, 2).

% Direction deltas
dir(up, -1, 0).
dir(down, 1, 0).
dir(left, 0, -1).
dir(right, 0, 1).

% Time steps (0 = initial state)
time(0..6).

% Previous time step relation
prev(T1, T2) :- time(T1), time(T2), T2 = T1 + 1.

% Initial positions
pos(a, 0, 1, 0).
pos(b, 1, 1, 0).

% At each time step T > 0, at most one robot makes one move
{ act(R, D, T) : robot(R), dir(D, _, _) } 0 1 :- time(T), T > 0.

% Compute target cell of a move
next_row(R, Nr, T) :- act(R, D, T), dir(D, Dr, _), pos(R, Rr, _, Tp), prev(Tp, T), Nr = Rr + Dr.
next_col(R, Nc, T) :- act(R, D, T), dir(D, _, Dc), pos(R, _, Rc, Tp), prev(Tp, T), Nc = Rc + Dc.

% Validate: within grid bounds
:- act(R, D, T), next_row(R, Nr, T), not row(Nr).
:- act(R, D, T), next_col(R, Nc, T), not col(Nc).

% Validate: no wall blocking the move
:- act(R, D, T), pos(R, Rr, Rc, Tp), prev(Tp, T), next_row(R, Nr, T), next_col(R, Nc, T),
   wall(Rr, Rc, Nr, Nc).

% Validate: target cell not occupied by another robot
:- act(R1, D, T), next_row(R1, Nr, T), next_col(R1, Nc, T),
   pos(R2, Nr, Nc, Tp), prev(Tp, T), R1 != R2.

% Update position for the moving robot
pos(R, Nr, Nc, T) :- act(R, D, T), next_row(R, Nr, T), next_col(R, Nc, T).

% Frame axiom: position persists for non-moving robots
pos(R, Rr, Rc, T) :- pos(R, Rr, Rc, Tp), prev(Tp, T), time(T), T > 0, not act(R, _, T).

% No two robots at same cell at same time
:- pos(R1, Rr, Rc, T), pos(R2, Rr, Rc, T), R1 < R2.

% Goal: Robot A must reach target at some time step
goal(T) :- pos(a, 2, 1, T), time(T).

% Must reach goal
:- not goal(_).

% Minimize total number of moves using weak constraint
:~ act(R, D, T). [1@1]

% === Output predicates ===

solution_found :- goal(_).

total_moves(N) :- N = #count { T : act(R, D, T) }.

% Sequence: from and to positions for each move
seq_from(R, Rr, Rc, T) :- act(R, D, T), pos(R, Rr, Rc, Tp), prev(Tp, T).
seq_to(R, Nr, Nc, T) :- act(R, D, T), next_row(R, Nr, T), next_col(R, Nc, T).

% Find earliest goal time
earlier_goal(T) :- goal(T2), T2 < T, time(T), time(T2).
min_goal_time(T) :- goal(T), not earlier_goal(T).

% Final positions at the moment goal is first reached
final_pos(R, Rr, Rc) :- pos(R, Rr, Rc, T), min_goal_time(T).

#show solution_found.
#show total_moves/1.
#show act/3.
#show seq_from/4.
#show seq_to/4.
#show final_pos/3.