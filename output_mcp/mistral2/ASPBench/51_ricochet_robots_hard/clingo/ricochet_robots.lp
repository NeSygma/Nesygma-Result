% --- Grid and Domain ---
cell(0..4, 0..4).
robot(a; b; c).
time(0..max_time).

% --- Initial Data ---
start_pos(a, 0, 1).
start_pos(b, 1, 1).
start_pos(c, 3, 1).
target(2, 3).

% --- Walls ---
% Column 0 right side: rows 0-4 (left boundary of starting corridor)
wall(0, 0, right).
wall(1, 0, right).
wall(2, 0, right).
wall(3, 0, right).
wall(4, 0, right).

% Column 1 right side: rows 0-1 and 3-4 (creates bridge opening at row 2)
wall(0, 1, right).
wall(1, 1, right).
wall(3, 1, right).
wall(4, 1, right).

% Column 2 right side: rows 0-1 and 3-4 (creates bridge opening at row 2)
wall(0, 2, right).
wall(1, 2, right).
wall(3, 2, right).
wall(4, 2, right).

% --- Helper Predicates ---
move_dir(R1, C1, R2, C2, right) :- R1 = R2, C2 = C1 + 1.
move_dir(R1, C1, R2, C2, left)  :- R1 = R2, C2 = C1 - 1.
move_dir(R1, C1, R2, C2, up)    :- C1 = C2, R2 = R1 - 1.
move_dir(R1, C1, R2, C2, down)  :- C1 = C2, R2 = R1 + 1.

valid_move(R1, C1, R2, C2) :-
    cell(R1, C1), cell(R2, C2),
    (R1 = R2, abs(C2 - C1) = 1) ;
    (C1 = C2, abs(R2 - R1) = 1).

% --- State and Moves ---
% Initial state
at(Rbt, R, C, 0) :- start_pos(Rbt, R, C).

% Choice rule for moves
{ sequence(M, Rbt, R1, C1, R2, C2) : robot(Rbt), cell(R1, C1), cell(R2, C2), valid_move(R1, C1, R2, C2) } 1 :- time(M), M > 0, M <= max_time.

% State transition
at(Rbt, R2, C2, T+1) :- sequence(T, Rbt, R1, C1, R2, C2), at(Rbt, R1, C1, T), time(T), T < max_time.
at(Rbt, R, C, T+1) :- at(Rbt, R, C, T), time(T), T < max_time, not moved(Rbt, T).
moved(Rbt, T) :- sequence(T, Rbt, _, _, _, _).

% No collisions
:- 2 { at(Rbt, R, C, T) : robot(Rbt) }, time(T).

% Wall blocking
:- sequence(M, Rbt, R1, C1, R2, C2), wall(R1, C1, Dir), move_dir(R1, C1, R2, C2, Dir).

% Final state: Robot A must be at the target position at the final time step
:- not at(a, 2, 3, N), moves(N).

% --- Objective ---
moves(N) :- time(N), at(a, 2, 3, N).
#minimize { N : moves(N) }.

% --- Output ---
solution_found :- moves(_).
final_pos(Rbt, R, C) :- at(Rbt, R, C, N), moves(N).

#show solution_found/0.
#show moves/1.
#show sequence/6.
#show final_pos/3.