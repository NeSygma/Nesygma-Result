% Robots and grid
robot(a). robot(b). robot(c).

% Grid size
row(0..4). col(0..4).

% Time horizon (allow up to 7 moves)
maxT(7).
time(0..7).

% Initial positions: pos(Robot, Row, Col, Time)
pos(a,0,1,0).
pos(b,1,1,0).
pos(c,3,1,0).

% Walls: vertical wall on the right side of Column at Row (wall blocks movement from column to column+1)
% column 0 right side rows 0-4
wall_right(0,0). wall_right(0,1). wall_right(0,2). wall_right(0,3). wall_right(0,4).
% column 1 right side rows 0-1 and 3-4 (bridge opening at row 2)
wall_right(1,0). wall_right(1,1). wall_right(1,3). wall_right(1,4).
% column 2 right side rows 0-1 and 3-4 (bridge opening at row 2)
wall_right(2,0). wall_right(2,1). wall_right(2,3). wall_right(2,4).

% Adjacency (Manhattan distance = 1) within grid bounds
adj(R,C,R,C1) :- row(R), col(C), col(C1), C1 = C+1, C1 <= 4.
adj(R,C,R,C1) :- row(R), col(C), col(C1), C1 = C-1, C1 >= 0.
adj(R,C,R1,C) :- col(C), row(R), row(R1), R1 = R+1, R1 <= 4.
adj(R,C,R1,C) :- col(C), row(R), row(R1), R1 = R-1, R1 >= 0.

% Blocked moves due to vertical walls
blocked(FR,FC,TR,TC) :- FR = TR, TC = FC+1, wall_right(FC,FR).   % moving right blocked
blocked(FR,FC,TR,TC) :- FR = TR, TC = FC-1, wall_right(TC,FR).   % moving left blocked

% Occupied cells at time T (by any robot)
occupied(Rr,Cc,T) :- pos(_,Rr,Cc,T).

% A move is possible if adjacent, not blocked, and target cell free at time T
possible_move(R,TR,TC,T) :-
    pos(R,FR,FC,T),
    adj(FR,FC,TR,TC),
    not blocked(FR,FC,TR,TC),
    not occupied(TR,TC,T).

% Exactly one robot moves at each step 0..maxT-1
1 { move(R,TR,TC,T) : possible_move(R,TR,TC,T) } 1 :- time(T), maxT(M), T < M.

% State transition (ensure next time is within horizon)
pos(R,TR,TC,T1) :- move(R,TR,TC,T), T1 = T+1, time(T1).
pos(R,FR,FC,T1) :- pos(R,FR,FC,T), not move(R,_,_,T), T1 = T+1, time(T1).

% No two robots may occupy the same cell at the same time
:- pos(R1,Rr,Cc,T), pos(R2,Rr,Cc,T), R1 != R2.

% Goal: Robot A at target (2,3) at final time maxT
:- maxT(M), not pos(a,2,3,M).

% Derive solution_found
solution_found :- maxT(M), pos(a,2,3,M).

% Count moves
moves(N) :- N = #count { T : move(_,_,_,T) }.

% Sequence information (from and to positions)
seq(T,R,FR,FC,TR,TC) :- move(R,TR,TC,T), pos(R,FR,FC,T).

% Final positions
final_pos(R,FR,FC) :- maxT(M), pos(R,FR,FC,M).

#show solution_found/0.
#show moves/1.
#show seq/6.
#show final_pos/3.