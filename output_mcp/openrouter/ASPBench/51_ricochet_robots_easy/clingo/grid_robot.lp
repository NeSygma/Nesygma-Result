% Domains
row(0..3). col(0..3).
robot(a). robot(b).

% Cells
cell(R,C) :- row(R), col(C).

% Initial positions at time 0
pos(a,0,1,0).
pos(b,1,1,0).

% Time horizon and steps
time(0..5).
step(0..4).

% Define next time relation
next(T,T1) :- time(T), T1 = T + 1, time(T1).

% Adjacent cells (Manhattan distance 1)
adjacent(R1,C1,R2,C2) :- row(R1), col(C1), row(R2), col(C2),
    (R1 = R2, C1 = C2 + 1 ; R1 = R2, C1 + 1 = C2 ; C1 = C2, R1 = R2 + 1 ; C1 = C2, R1 + 1 = R2).

% Walls: vertical wall between column 2 and 3 for rows 0 and 1
blocked(0,2,0,3).
blocked(1,2,1,3).
blocked(0,3,0,2).
blocked(1,3,1,2).

% Choice of a move at each step (0 or 1 move per step)
0 { move(S,R,FR,FC,TR,TC) : robot(R), cell(FR,FC), cell(TR,TC), adjacent(FR,FC,TR,TC), not blocked(FR,FC,TR,TC) } 1 :- step(S).

% Ensure the robot moves from its current position
:- move(S,R,FR,FC,_,_), not pos(R,FR,FC,S).

% Update positions after a move
pos(R,TR,TC,T1) :- move(T,R,_,_,TR,TC), step(T), next(T,T1).
% Persistence when no move for this robot at this step
pos(R,Rr,Cc,T1) :- pos(R,Rr,Cc,T), not move(T,R,_,_,_,_), step(T), next(T,T1).

% No two robots share a cell at the same time
:- pos(R1,Rr,Cc,T), pos(R2,Rr,Cc,T), R1 != R2, time(T).

% Goal: robot A at target (2,1) at final time 5
:- not pos(a,2,1,5).

% Count moves
moves(N) :- N = #count { S,R,FR,FC,TR,TC : move(S,R,FR,FC,TR,TC) }.

% Solution found flag
solution_found :- pos(a,2,1,5).

% Final positions (at time 5)
final_pos(R,Rr,Cc) :- pos(R,Rr,Cc,5).

% Primary optimization: minimize number of moves
#minimize { 1,S : move(S,_,_,_,_,_) }.
% Secondary optimization: minimize final column of B (prefer smaller column)
#minimize { 1,C : final_pos(b,_,C) }.

#show solution_found/0.
#show moves/1.
#show move/6.
#show final_pos/3.