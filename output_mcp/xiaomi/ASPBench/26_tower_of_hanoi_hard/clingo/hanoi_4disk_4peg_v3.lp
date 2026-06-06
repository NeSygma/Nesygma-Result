% Tower of Hanoi with 4 disks, 4 pegs
% Every disk must visit pegs B and C during journey from A to D

% ============ DOMAIN DEFINITIONS ============
% Disks: 1 (smallest) to 4 (largest)
disk(1). disk(2). disk(3). disk(4).

% Pegs
peg(a). peg(b). peg(c). peg(d).

% Time steps: we need enough for optimal solution
time(0..25).

% ============ INITIAL STATE ============
% All disks start on peg A, stacked 4(bottom),3,2,1(top)
on(4, a, 0).
on(3, a, 0).
on(2, a, 0).
on(1, a, 0).

% ============ ACTIONS ============
% At each time step, exactly one disk moves from one peg to another
% move(D, From, To, T) means disk D moves from peg From to peg To at time T

% Generate possible moves
{ move(D, From, To, T) : disk(D), peg(From), peg(To), From != To } 1 :- time(T), T > 0.

% ============ STATE PERSISTENCE ============
% Disk D is on peg P at time T if it was moved there at T-1
on(D, P, T) :- move(D, _, P, T-1), time(T).

% Disk D stays on peg P at time T if it was there at T-1 and not moved away
on(D, P, T) :- on(D, P, T-1), time(T), not move(D, P, _, T-1).

% ============ PRECONDITIONS ============

% Disk D is on top of peg P at time T if it's on P and no smaller disk is on P
top(D, P, T) :- on(D, P, T), disk(D), peg(P), time(T),
                 not exists_smaller_on(D, P, T).

exists_smaller_on(D, P, T) :- on(D2, P, T), disk(D2), disk(D), peg(P), time(T),
                               D2 < D.

% Precondition: disk being moved must be on top of source peg
:- move(D, From, To, T), not top(D, From, T-1).

% ============ EFFECTS ============

% After move, disk is no longer on source peg
:- move(D, From, To, T), on(D, From, T).

% After move, disk is on destination peg
:- move(D, From, To, T), not on(D, To, T).

% ============ CONSTRAINTS ============

% Larger disk cannot be placed on smaller disk
:- move(D, _, To, T), on(D2, To, T), disk(D), disk(D2), peg(To), time(T),
   D > D2.

% ============ JOURNEY CONSTRAINT ============
% Every disk must land on peg B at least once
visited_b(D) :- move(D, _, b, T), disk(D), time(T).
:- disk(D), not visited_b(D).

% Every disk must land on peg C at least once
visited_c(D) :- move(D, _, c, T), disk(D), time(T).
:- disk(D), not visited_c(D).

% ============ GOAL STATE ============
% All disks must be on peg D at the end
:- disk(D), not on(D, d, 25).

% ============ OPTIMIZATION ============
% Minimize total number of moves
#minimize { 1, D, From, To, T : move(D, From, To, T) }.

% ============ OUTPUT ============
#show move/4.