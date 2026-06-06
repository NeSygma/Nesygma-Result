% Ricochet Robots - Minimal debug
% Remove finished constraint, just check if moves can be made

time(0..5).
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

% Show which moves are valid at time 0
% Check: robot A at (0,1), valid moves from (0,1)
test_move_a(R2,C2) :- valid_move(0,1,R2,C2).
% Check: robot B at (1,1), valid moves from (1,1)
test_move_b(R2,C2) :- valid_move(1,1,R2,C2).
% Check: robot C at (3,1), valid moves from (3,1)
test_move_c(R2,C2) :- valid_move(3,1,R2,C2).

% Also check blocked moves
test_blocked(R1,C1,R2,C2) :- blocked(R1,C1,R2,C2), adj(R1,C1,R2,C2).

#show test_move_a/2.
#show test_move_b/2.
#show test_move_c/2.
#show test_blocked/4.
#show wall_right/2.