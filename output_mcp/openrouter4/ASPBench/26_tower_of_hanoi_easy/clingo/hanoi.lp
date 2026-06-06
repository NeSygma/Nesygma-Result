%%% Tower of Hanoi - 4 disks, 3 pegs %%%

% Constants
disk(1..4).
peg(a;b;c).

% Time horizon (optimal is 15 moves)
time(0..15).

%%% Initial State %%%
% Initially all disks on peg A (4 bottom, 1 top)
on(4, a, 0).
on(3, a, 0).
on(2, a, 0).
on(1, a, 0).

%%% Helper Predicates %%%

% A disk has a smaller disk on the same peg
has_smaller(D, P, T) :- on(D, P, T), on(D2, P, T), D2 < D.

% A disk is top of a peg if no smaller disk is on the same peg
top(D, P, T) :- on(D, P, T), not has_smaller(D, P, T).

% A peg has at least one disk
has_disk(P, T) :- on(_, P, T).

% A disk can be placed on a peg if the peg is empty
can_place(D, P, T) :- disk(D), peg(P), time(T), not has_disk(P, T).

% A disk can be placed on a peg if the top disk is larger
can_place(D, P, T) :- disk(D), peg(P), time(T), top(D2, P, T), D < D2.

%%% Action Generation %%%
% At most one move per time step
{ move(D, F, T_peg, Time) : disk(D), peg(F), peg(T_peg), F != T_peg } 1 :- time(Time), Time < 15.

%%% Preconditions %%%
% Can only move a disk that is top of its source peg
:- move(D, F, T_peg, Time), not top(D, F, Time).

% Can only move a disk to a peg where it can be placed
:- move(D, F, T_peg, Time), not can_place(D, T_peg, Time).

%%% Effects %%%
% Disk moves to destination peg
on(D, T_peg, Time+1) :- move(D, F, T_peg, Time), time(Time+1).

% Frame: disk stays on same peg unless moved away from it
on(D, P, Time+1) :- on(D, P, Time), time(Time+1), not move(D, P, _, Time).

%%% State Constraints %%%
% Each disk must be on exactly one peg at each time
:- disk(D), time(T), #count{P : on(D, P, T)} != 1.

%%% Goal State %%%
% All disks must be on peg C at the final time
:- disk(D), not on(D, c, 15).

%%% Minimize number of moves %%%
#minimize { 1,Time : move(_, _, _, Time) }.

%%% Output %%%
#show move/4.