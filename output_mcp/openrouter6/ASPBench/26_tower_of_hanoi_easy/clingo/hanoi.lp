% Tower of Hanoi with 4 disks, 3 pegs
% Minimize number of moves

% Domains
disk(1..4).
peg(a). peg(b). peg(c).
time(0..20).  % enough for optimal 15 moves

% Size ordering (larger number = larger disk)
size(1,1). size(2,2). size(3,3). size(4,4).

% Initial state at time 0
on(1,a,0). on(2,a,0). on(3,a,0). on(4,a,0).

% Move predicate: move(Disk, FromPeg, ToPeg, Time)
{ move(D,From,To,T) : disk(D), peg(From), peg(To), From != To } 1 :- time(T), T > 0.

% Validity constraints for moves
% 1. Disk must be on source peg at previous time
:- move(D,From,To,T), not on(D,From,T-1).

% 2. Disk must be top on source peg (no smaller disk on same peg)
:- move(D,From,To,T), on(E,From,T-1), size(E) < size(D).

% 3. Cannot place on larger or equal disk on destination peg
:- move(D,From,To,T), on(E,To,T-1), size(E) <= size(D).

% Frame axioms: state persistence
% If no move affects disk D on peg P, then it stays there
on(D,P,T) :- not move(D,_,_,T), on(D,P,T-1), time(T), T > 0.

% If disk D moves to peg P at time T, then it's on P at T
on(D,P,T) :- move(D,_,P,T).

% Goal state: all disks on peg c
goal(T) :- on(1,c,T), on(2,c,T), on(3,c,T), on(4,c,T).

% Last move time: maximum time where a move occurs
last_move_time(T) :- T = #max{ T2 : move(_,_,_,T2) }.

% Constraint: goal must be reached at last move time
:- last_move_time(T), not goal(T).

% Minimize the last move time (equivalent to minimizing moves)
#minimize { T@1 : last_move_time(T) }.

% Compute total moves
total_moves(N) :- N = #count{ D,From,To,T : move(D,From,To,T) }.

% Check optimality (15 moves for 4 disks)
is_optimal :- total_moves(15).

% Output directives
#show move/4.
#show total_moves/1.
#show is_optimal/0.
#show goal/1.
#show last_move_time/1.