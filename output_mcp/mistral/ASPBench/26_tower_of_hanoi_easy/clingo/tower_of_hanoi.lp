% Disks and pegs
 disk(1..4).
 peg("A"). peg("B"). peg("C").

% Time steps (0 to 15)
 time(0..15).

% Initial state: disks stacked on peg A (4 at bottom, 1 at top)
% Disk 1 is on top of disk 2, which is on top of disk 3, etc.
on(1, "A", 0).
on(2, "A", 0) :- on(1, "A", 0).
on(3, "A", 0) :- on(2, "A", 0).
on(4, "A", 0) :- on(3, "A", 0).

% Goal state: all disks on peg C (4 at bottom, 1 at top)
% We'll check this at time 15

% Define top disk on each peg at each time step
% A disk is on top if there's no disk above it on the same peg
top(D, P, T) :- on(D, P, T), not on(D2, P, T) : disk(D2), D2 > D, time(T).

% A disk can be moved if it is the top disk on its peg
can_move(D, From, T) :- top(D, From, T), time(T), T < 15.

% A move is valid if the destination peg is empty or the top disk on the destination peg is larger than the disk being moved
valid_move(D, From, To, T) :- can_move(D, From, T), peg(To), From != To, time(T), T < 15,
                                not on(_, To, T). % Destination peg is empty

valid_move(D, From, To, T) :- can_move(D, From, T), peg(To), From != To, time(T), T < 15,
                                top(D2, To, T), D < D2. % Destination peg has a larger disk on top

% Choice rule: decide which valid move to make at each time step
 { move(D, From, To, T) : valid_move(D, From, To, T) } 1 :- time(T), T < 15.

% Constraints on moves
 :- move(D1, From1, To1, T), move(D2, From2, To2, T), D1 != D2, time(T), T < 15. % Only one move per time step
 :- move(D, From, To, T), not valid_move(D, From, To, T), time(T), T < 15. % Only valid moves are allowed

% State transition: update the state after a move
% When a disk is moved, it's no longer on the source peg
% When a disk is moved, it's now on the destination peg
% All other disks remain in their positions

% Disk is on destination peg after move
on(D, To, T+1) :- move(D, From, To, T), time(T), T < 15.

% Disk is not on source peg after move (unless it was moved back)
on(D, From, T+1) :- on(D, From, T), not move(D, From, _, T), time(T), T < 15.

% Ensure no disk is placed on a smaller disk (this is enforced by valid_move)

% Goal condition: all disks must be on peg C at time 15, in the correct order
% We need to check that disk 4 is at the bottom, then 3, then 2, then 1 on top
goal_reached :- on(4, "C", 15), on(3, "C", 15), on(2, "C", 15), on(1, "C", 15).

% Display the solution
#show move/4.
#show goal_reached/0.

% Optional: Show total moves and optimality
total_moves(M) :- M = #count{ T : time(T), T < 15, move(_,_,_,T) }.
is_optimal :- total_moves(15), goal_reached.
#show total_moves/1.
#show is_optimal/0.