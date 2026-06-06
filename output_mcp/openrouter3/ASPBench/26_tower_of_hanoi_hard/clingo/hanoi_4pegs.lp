% Tower of Hanoi with 4 disks, 4 pegs, and mandatory visits to B and C
% Disks: 1 (smallest) to 4 (largest)
% Pegs: A, B, C, D

% Domain declarations
disk(1..4).
peg("A"). peg("B"). peg("C"). peg("D").
time(0..20). % Sufficient time horizon for optimal solution

% Initial state: all disks on peg A
on(1, "A", 0).
on(2, "A", 0).
on(3, "A", 0).
on(4, "A", 0).

% Goal state: all disks on peg D
goal(D) :- disk(D), on(D, "D", T).

% Track which disks have visited B and C
visited_b(D) :- on(D, "B", T), T > 0.
visited_c(D) :- on(D, "C", T), T > 0.

% Choice rule: generate possible moves at each time step
% Exactly one move per time step
{ move(D, From, To, T) : disk(D), peg(From), peg(To), From != To } 1 :- time(T), T > 0.

% Precondition: disk must be on source peg at previous time
:- move(D, From, To, T), not on(D, From, T-1).

% Precondition: destination peg must be empty or have larger disk on top
% For each move, check that no smaller disk is on destination peg at time T-1
:- move(D, From, To, T), on(Small, To, T-1), Small < D.

% Effect: disk moves to destination peg at time T
on(D, To, T) :- move(D, From, To, T).

% Frame axiom: disks stay where they are unless moved
on(D, Peg, T) :- on(D, Peg, T-1), time(T), T > 0,
                 not move(D, _, Peg, T),  % Disk D is not moved TO Peg at time T
                 not move(D, Peg, _, T).   % Disk D is not moved FROM Peg at time T

% Constraint: exactly one disk moves at each time step
% (Already enforced by choice rule with cardinality 1)

% Constraint: a disk cannot be moved to the same peg it's already on
:- move(D, Peg, Peg, T).

% Track total moves
total_moves(N) :- N = #count{T : move(_, _, _, T)}.

% Objective: minimize total moves
#minimize { 1,T : move(_, _, _, T) }.

% Show solution
#show move/4.
#show total_moves/1.

% Show which disks have visited B and C
#show visited_b/1.
#show visited_c/1.

% Show final state
#show on/3.