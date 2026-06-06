% Tower of Hanoi with 4 disks and 4 pegs, with mandatory visits to B and C
% Disks: 1 (smallest) to 4 (largest)
% Pegs: "A", "B", "C", "D"

% Domain declarations
disk(1..4).
peg("A"; "B"; "C"; "D").

% Time steps: optimal is 19, so use 0..19
time(0..19).

% Initial state: all disks on peg A
on(1, "A", 0).
on(2, "A", 0).
on(3, "A", 0).
on(4, "A", 0).

% Top disk on each peg at time 0
top(1, "A", 0).

% Empty pegs at time 0
empty("B", 0).
empty("C", 0).
empty("D", 0).

% Move generation: at each time step, choose exactly one move
% Only generate moves that are potentially useful
1 { move(Disk, From, To, T) : disk(Disk), peg(From), peg(To), From != To } 1 :- time(T), T > 0.

% Precondition: Disk must be top on From peg at previous time
:- move(Disk, From, To, T), not top(Disk, From, T-1).

% Precondition: To peg must be empty or have larger top disk
:- move(Disk, From, To, T), not empty(To, T-1), not top(TopTo, To, T-1), Disk < TopTo.

% Frame axioms: persistence for on/above/top/empty
on(D, P, T) :- on(D, P, T-1), not move(D, P, _, T), not move(_, _, P, T).
top(D, P, T) :- top(D, P, T-1), not move(D, _, _, T), not move(_, _, P, T).
empty(P, T) :- empty(P, T-1), not move(_, _, P, T).

% Update on after move
on(Disk, To, T) :- move(Disk, From, To, T).

% Update top after move
top(Disk, To, T) :- move(Disk, From, To, T).

% Update empty after move
empty(Peg, T) :- empty(Peg, T-1), not move(_, _, Peg, T).

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