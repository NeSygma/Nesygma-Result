% --- Facts ---
disk(1..4).
peg(a; b; c; d).

% --- Time Horizon ---
% Use a sufficiently large horizon to allow for the optimal solution (19 moves)
time(0..25).

% --- Initial State ---
% At time 0, disks 1-4 are stacked on peg A in order (disk 4 at bottom, disk 1 on top)
on(D, a, 0) :- disk(D).

% --- Helper Predicates ---
% top(D, P, T): Disk D is the top disk of peg P at time T
top(D, P, T) :-
    on(D, P, T),
    not other_disk_on_top(D, P, T).

other_disk_on_top(D2, P, T) :-
    on(D, P, T),
    on(D2, P, T),
    D < D2.

% --- Choice Rule: Generate Moves ---
% At each time step, choose a disk to move from its current peg to another peg
{ move(D, From, To, T) : disk(D), peg(From), peg(To), From != To } 1 :- time(T), T > 0.

% --- Constraints ---
% 1. Only the top disk can be moved
:- move(D, From, To, T), not top(D, From, T).

% 2. Larger disk cannot be placed on smaller disk
:- move(D, From, To, T),
   on(D2, To, T-1),
   D < D2.

% 3. Update state after a move
% Disk D is on peg To at time T if it was moved to To at time T
on(D, To, T) :- move(D, From, To, T).
% All other disks remain in their previous positions unless moved
on(D, P, T) :- on(D, P, T-1), not moved_from(D, P, T).

moved_from(D, P, T) :- move(D, P, _, T).

% --- Pilgrim's Journey ---
% Every disk must land on peg B and peg C at least once
visited(D, P) :- move(D, _, P, _).

% --- Ensure all disks visit B and C at least once ---
:- disk(D), not visited(D, b).
:- disk(D), not visited(D, c).

% --- Goal State ---
% At the final time step, all disks must be on peg D in the correct order
:- not all_disks_on_d_at_final_time.

all_disks_on_d_at_final_time :-
    on(1, d, 25),
    on(2, d, 25),
    on(3, d, 25),
    on(4, d, 25).

% --- Objective: Minimize the total number of moves ---
total_moves(N) :- N = #count { T : time(T), T > 0, move(_, _, _, T) }.

% --- Show the moves and total moves ---
#show move/4.
#show total_moves/1.