% Tower of Hanoi with 4 disks and 3 pegs
% Solve using ASP with minimization

% Domain declarations
disk(1..4).
peg("A"; "B"; "C").
time(0..15).  % Maximum 15 moves for optimal solution

% Initial state: All disks on peg A in order [4,3,2,1] (bottom to top)
% We model this by having disk D on peg A at time 0
on(1, "A", 0).
on(2, "A", 0).
on(3, "A", 0).
on(4, "A", 0).

% Top disk at time 0 is disk 1 (smallest)
top(1, "A", 0).

% Goal state: All disks on peg C in same order at final time
% We'll enforce this through constraints

% Choice rule: At each time step, we can move one disk from one peg to another
{ move(D, P1, P2, T) : disk(D), peg(P1), peg(P2), P1 != P2 } 1 :- time(T), T < 15.

% Constraint: Cannot move from empty peg
:- move(D, P1, P2, T), not on(D, P1, T).

% Constraint: Only top disk can move
:- move(D, P1, P2, T), top(D2, P1, T), D != D2.

% Constraint: Cannot place larger disk on smaller disk
% For each move, check that destination peg's top disk (if any) is larger than moved disk
:- move(D, P1, P2, T), top(D2, P2, T), D2 < D.

% Frame axioms: State persists unless changed by a move
on(D, P, T+1) :- on(D, P, T), time(T), time(T+1), not move(D, P, _, T).
on(D, P2, T+1) :- move(D, P1, P2, T), time(T), time(T+1).

% Update top disk after move
% If a disk moves from P1, the new top is the next smaller disk on P1
top(D2, P1, T+1) :- move(D, P1, _, T), on(D2, P1, T), D2 < D, 
                     not (on(D3, P1, T), D3 < D, D3 > D2), time(T), time(T+1).

% If a disk moves to P2, it becomes the new top
top(D, P2, T+1) :- move(D, _, P2, T), time(T), time(T+1).

% If no disk moves to/from a peg, top persists
top(D, P, T+1) :- top(D, P, T), time(T), time(T+1), 
                  not move(D, P, _, T), not move(_, _, P, T).

% Constraint: At most one move per time step (already enforced by choice rule)

% Goal constraint: At final time (after all moves), all disks must be on peg C
% We'll find the actual final time from the moves
final_time(T) :- T = #max { T2 : move(_, _, _, T2) }.
:- not final_time(_).  % Ensure at least one move occurs

% Enforce goal state at final time
:- final_time(T), on(D, P, T), P != "C".

% Ensure disks are in correct order on peg C at final time
% Disk 4 must be at bottom, then 3, then 2, then 1 on top
% We can check this by ensuring no larger disk is on top of a smaller one
:- final_time(T), on(D1, "C", T), on(D2, "C", T), D1 < D2, 
   not (on(D3, "C", T), D3 > D1, D3 < D2).  % D1 is directly above D2

% Count total moves
total_moves(N) :- N = #count { D, P1, P2, T : move(D, P1, P2, T) }.

% Minimize number of moves
#minimize { 1, T : move(_, _, _, T) }.

% Show solution
solution_exists :- move(_, _, _, _).
#show solution_exists.
#show total_moves/1.
#show move/4.
#show on/3.
#show top/3.