% --- Facts ---
disk(1..4).
peg(a; b; c).
time(0..15).

% --- Initial State ---
% At time 0, disks 4,3,2,1 are on peg A (bottom to top)
on_peg(4, a, 0).
on_peg(3, a, 0).
on_peg(2, a, 0).
on_peg(1, a, 0).

% --- Helper Predicates ---
% top_disk(P, D, T): Disk D is the top disk of peg P at time T
top_disk(P, D, T) :-
    on_peg(D, P, T),
    not smaller_disk_on_peg(D, P, T).

% smaller_disk_on_peg(D, P, T): There exists a disk smaller than D on peg P at time T
smaller_disk_on_peg(D, P, T) :-
    on_peg(D2, P, T),
    on_peg(D, P, T),
    D2 < D.

% --- Move Generation ---
% move(D, From, To, T): Disk D is moved from From to To at time T
{ move(D, From, To, T) : disk(D), peg(From), peg(To) } 1 :- time(T), T > 0.

% --- Move Validity ---
% A disk can only be moved if it is the top disk of its peg
valid_move(D, From, To, T) :-
    move(D, From, To, T),
    top_disk(From, D, T-1),
    time(T-1).

% A disk can only be moved to a peg where it is smaller than the top disk (or the peg is empty)
valid_move(D, From, To, T) :-
    move(D, From, To, T),
    top_disk(To, D2, T-1),
    D < D2,
    time(T-1).

% A disk can be moved to an empty peg
valid_move(D, From, To, T) :-
    move(D, From, To, T),
    not top_disk(To, _, T-1),
    time(T-1).

% --- State Transition ---
% Disk is moved to the destination peg if the move is valid
on_peg(D, To, T) :-
    move(D, From, To, T),
    valid_move(D, From, To, T),
    time(T).

% Disk is removed from the source peg if the move is valid
:- move(D, From, To, T),
   on_peg(D, From, T),
   valid_move(D, From, To, T),
   time(T).

% Disks not moved stay on their pegs
on_peg(D, P, T) :-
    on_peg(D, P, T-1),
    not move(D, P, _, T),
    time(T).

% --- Goal State ---
% All disks are on peg C at time 15, in order
goal_reached :-
    on_peg(4, c, 15),
    on_peg(3, c, 15),
    on_peg(2, c, 15),
    on_peg(1, c, 15).

% --- Constraints ---
% Only valid moves are allowed
:- move(D, From, To, T), not valid_move(D, From, To, T).

% Ensure the goal is reached
:- not goal_reached.

% --- Optimization: Exactly 15 moves ---
% Count the number of moves
total_moves(N) :- N = #count { D, From, To, T : move(D, From, To, T) }.

% Enforce exactly 15 moves (optimal solution)
:- total_moves(N), N != 15.

% --- Output ---
#show move/4.
#show total_moves/1.
#show is_optimal :- total_moves(15).