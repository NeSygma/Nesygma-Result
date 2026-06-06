% Tower of Hanoi - 4 disks, 3 pegs
% Find optimal solution (15 moves)

% ============ DOMAINS ============
% Disks: 1 (smallest) to 4 (largest)
disk(1..4).

% Pegs
peg(a). peg(b). peg(c).

% Time steps: 0 (initial) to 15 (max moves)
time(0..15).

% Disk size ordering (larger number = larger disk)
larger(D2, D1) :- disk(D1), disk(D2), D2 > D1.

% ============ INITIAL STATE ============
% All disks start on peg A
on(1, a, 0).
on(2, a, 0).
on(3, a, 0).
on(4, a, 0).

% ============ CHOICE RULES ============
% At each time step, optionally move one disk
{ move(D, From, To, T) : disk(D), peg(From), peg(To), From != To } 1 :- time(T), T > 0.

% ============ PRECONDITIONS ============
% A disk can only be moved if it's on top of its peg
% A disk is on top if no smaller disk is on the same peg
top(D, P, T) :- on(D, P, T), not blocked(D, P, T).
blocked(D, P, T) :- on(D, P, T), on(D2, P, T), larger(D, D2).

% Can only move the top disk
:- move(D, From, To, T), not top(D, From, T-1).

% Cannot place disk on a smaller disk
:- move(D, _, To, T), on(D2, To, T-1), larger(D, D2).

% ============ EFFECTS (STATE CHANGE) ============
% Disk moves to new peg
on(D, To, T) :- move(D, _, To, T), time(T), T > 0.

% Disk stays on same peg if not moved
on(D, P, T) :- on(D, P, T-1), time(T), T > 0, not move(D, P, _, T).

% Disk leaves old peg when moved
:- move(D, From, To, T), on(D, From, T).

% ============ GOAL STATE ============
% All disks must be on peg C at the end
:- not on(D, c, 15), disk(D).

% ============ OPTIMIZATION ============
% Minimize total number of moves
#minimize { 1, D, From, To, T : move(D, From, To, T) }.

% ============ SYMMETRY BREAKING ============
% Prefer moving to peg c over b when possible (helps search)
% This is optional but helps find solution faster

% ============ OUTPUT ============
#show move/4.