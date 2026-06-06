% Tower of Hanoi with 4 disks and 3 pegs
% Find optimal solution (minimum moves)

% ============ DOMAIN DEFINITIONS ============
% Disks: 1 (smallest) to 4 (largest)
disk(1). disk(2). disk(3). disk(4).

% Pegs: A (source), B (auxiliary), C (destination)
peg(a). peg(b). peg(c).

% Time steps: 0 to max_time (15 moves needed for 4 disks)
time(0..15).

% Disk sizes (larger number = larger disk)
size(1, 1). size(2, 2). size(3, 3). size(4, 4).

% ============ INITIAL STATE ============
% At time 0, all disks are on peg A
on(disk, peg, 0) :- disk(D), size(D, _), peg(a).

% ============ GOAL STATE ============
% All disks must be on peg C at the final time
goal :- time(15), {on(D, c, 15) : disk(D)} = 4.

% ============ ACTIONS ============
% At each time step, we can move one disk from one peg to another
{move(D, From, To, T) : disk(D), peg(From), peg(To)} 1 :- time(T), T > 0.

% ============ PRECONDITIONS ============
% Can only move a disk if it's on top of its current peg
% A disk is on top if no smaller disk is on the same peg
top(D, P, T) :- on(D, P, T), disk(D), peg(P), time(T),
                 not {on(D2, P, T) : disk(D2), size(D2, S2), size(D, S), S2 < S} > 0.

% Can only move a disk that is on top of its source peg
:- move(D, From, To, T), not top(D, From, T-1).

% Cannot move a disk to a peg where a smaller disk exists
:- move(D, From, To, T), on(D2, To, T-1), disk(D2), size(D, S1), size(D2, S2), S1 > S2.

% Cannot move a disk to the same peg
:- move(D, P, P, T).

% ============ EFFECTS ============
% After a move, the disk is on the destination peg
on(D, To, T) :- move(D, From, To, T).

% After a move, the disk is no longer on the source peg
not_on(D, From, T) :- move(D, From, To, T).

% Frame axiom: disk stays on peg if not moved
on(D, P, T) :- on(D, P, T-1), time(T), T > 0, 
               not not_on(D, P, T).

% ============ CONSTRAINTS ============
% Only one disk can be moved at a time (already enforced by choice rule)

% All disks must end on peg C
:- time(15), disk(D), not on(D, c, 15).

% ============ OPTIMIZATION ============
% Minimize the number of moves
#minimize {1, D, From, To, T : move(D, From, To, T)}.

% ============ OUTPUT ============
#show move/4.
#show on/3.