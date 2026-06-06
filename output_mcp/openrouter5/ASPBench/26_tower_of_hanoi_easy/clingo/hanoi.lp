%% Tower of Hanoi - 4 disks, 3 pegs
%% Find optimal solution minimizing moves

%% Time horizon: optimal is 15 moves, so we need at most 15 time steps
time(0..15).

%% Disks 1 (smallest) to 4 (largest)
disk(1..4).

%% Pegs
peg(a; b; c).

%% Initial state: peg A has disks [4,3,2,1] bottom to top
%% We model on(disk, peg, time) meaning disk is on peg at time
%% Initial at time 0
on(4, a, 0).
on(3, a, 0).
on(2, a, 0).
on(1, a, 0).

%% No disks on B or C initially
:- disk(D), on(D, b, 0).
:- disk(D), on(D, c, 0).

%% Goal: all disks on peg C at final time
goal_time(15).
:- goal_time(T), disk(D), not on(D, c, T).

%% Each disk is on exactly one peg at each time
1 { on(D, P, T) : peg(P) } 1 :- disk(D), time(T).

%% --- Action modeling ---
%% move(D, From, To, T): disk D moves from peg From to peg To at time T (starting move at T, arriving at T+1)
{ move(D, From, To, T) : peg(From), peg(To), From != To } :- disk(D), time(T), T < 15.

%% At most one move per time step
:- #count { D, From, To : move(D, From, To, T) } > 1, time(T), T < 15.

%% Exactly one move per time step (to reach optimal, we need a move at each step)
1 { move(D, From, To, T) : disk(D), peg(From), peg(To), From != To } 1 :- time(T), T < 15.

%% Precondition: disk D must be on peg From at time T to move from there
:- move(D, From, To, T), not on(D, From, T).

%% Precondition: disk D must be the top disk on peg From at time T
%% Top disk means no smaller disk is on the same peg
:- move(D, From, To, T), disk(S), S < D, on(S, From, T).

%% Precondition: disk D cannot be placed on a smaller disk
%% i.e., if there is a disk S on peg To at time T, D must be smaller than S
:- move(D, From, To, T), disk(S), on(S, To, T), D > S.

%% Effects: after move, disk D is on peg To at time T+1
on(D, To, T+1) :- move(D, From, To, T), time(T+1).

%% Frame axiom: disks not moved stay where they are
on(D, P, T+1) :- on(D, P, T), time(T+1), not moved_off(D, P, T).

%% Helper: disk D moved off peg P at time T
moved_off(D, P, T) :- move(D, P, To, T).

%% --- Optimization: minimize total moves ---
%% Since we force exactly one move per step up to goal_time, we minimize the final time
#minimize { T : goal_time(T) }.

%% Show the moves in order
#show move/4.
#show total_moves/1.
#show is_optimal/1.

%% Compute total moves and optimality
total_moves(T) :- goal_time(T).
is_optimal :- total_moves(15).