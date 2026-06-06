% Tower of Hanoi with 4 disks and 4 pegs, with mandatory visits to B and C
% Disks: 1 (smallest) to 4 (largest)
% Pegs: "A", "B", "C", "D"

% Domain declarations
disk(1..4).
peg("A"; "B"; "C"; "D").

% Time steps: we'll use a bounded horizon, then minimize the number of moves
time(0..30).  % Maximum 30 moves, should be enough

% Initial state: all disks on peg A, with disk 1 on top
on(1, "A", 0).
on(2, "A", 0).
on(3, "A", 0).
on(4, "A", 0).

% Above relationships: disk1 is directly above disk2
above(1, 2, 0).
above(2, 3, 0).
above(3, 4, 0).

% Top disk on each peg at time 0
top(1, "A", 0).

% Empty pegs at time 0
empty("B", 0).
empty("C", 0).
empty("D", 0).

% Move generation: at each time step, choose exactly one move
1 { move(Disk, From, To, T) : disk(Disk), peg(From), peg(To), From != To } 1 :- time(T), T > 0.

% Precondition: Disk must be top on From peg at previous time
:- move(Disk, From, To, T), not top(Disk, From, T-1).

% Precondition: To peg must be empty OR Disk must be smaller than top on To peg
:- move(Disk, From, To, T), not empty(To, T-1), top(TopTo, To, T-1), Disk >= TopTo.

% Effects: update on/above/top/empty after a move
% Disk is no longer on From peg
on(Disk, From, T) :- move(Disk, From, To, T), not on(Disk, From, T).
% Disk is now on To peg
on(Disk, To, T) :- move(Disk, From, To, T).

% Update above relationships
% If To was empty, Disk becomes bottom (no above relationship)
% If To had a top disk TopTo, Disk becomes above TopTo
above(Disk, TopTo, T) :- move(Disk, From, To, T), top(TopTo, To, T-1), not empty(To, T-1).
% Remove previous above relationship for Disk (if any)
:- above(Disk, X, T-1), move(Disk, From, To, T), above(Disk, X, T).
% Remove previous above relationship where Disk was below another disk
:- above(Y, Disk, T-1), move(Disk, From, To, T), above(Y, Disk, T).

% Update top: Disk becomes top on To peg
top(Disk, To, T) :- move(Disk, From, To, T).
% Remove previous top on From peg
:- top(Disk, From, T-1), move(Disk, From, To, T), top(Disk, From, T).
% Remove previous top on To peg (if any)
:- top(OldTop, To, T-1), move(Disk, From, To, T), top(OldTop, To, T).

% Update empty status
empty(Peg, T) :- empty(Peg, T-1), not move(_, _, Peg, T).
:- empty(Peg, T-1), move(_, _, Peg, T), empty(Peg, T).

% Frame axioms: persistence for on/above/top/empty
on(D, P, T) :- on(D, P, T-1), not move(D, P, _, T), not move(_, _, P, T).
above(D1, D2, T) :- above(D1, D2, T-1), not move(D1, _, _, T), not move(D2, _, _, T).
top(D, P, T) :- top(D, P, T-1), not move(D, _, _, T), not move(_, _, P, T).
empty(P, T) :- empty(P, T-1), not move(_, _, P, T).

% Journey constraints: each disk must visit peg B and peg C at least once
% A disk "visits" a peg when it is moved to that peg (destination of a move)
visit(Disk, Peg, T) :- move(Disk, _, Peg, T).

% Each disk must have at least one visit to B and one to C
:- disk(D), not visit(D, "B", _).
:- disk(D), not visit(D, "C", _).

% Goal state: all disks on peg D at some time T
goal(T) :- on(1, "D", T), on(2, "D", T), on(3, "D", T), on(4, "D", T).

% Minimize the number of moves (i.e., the time step when goal is reached)
#minimize { T@1 : goal(T) }.

% Show the solution
#show move/4.
#show total_moves/1.
total_moves(T) :- goal(T), not goal(T-1).