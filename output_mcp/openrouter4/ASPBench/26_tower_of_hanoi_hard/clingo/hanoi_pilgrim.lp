%% Tower of Hanoi with 4 disks, 4 pegs, and Pilgrim's Journey constraint

%% Domain
disk(1..4).
peg(a;b;c;d).

%% Upper bound on moves (expected optimal is 19)
#const max_moves = 25.

step(1..max_moves).
time(0..max_moves).

%% Initial state: all disks on peg A at time 0
on(4, a, 0).
on(3, a, 0).
on(2, a, 0).
on(1, a, 0).

%% Clear/top helper
%% A disk is clear (top) if no smaller disk is on the same peg
blocked(D, T) :- on(D, P, T), on(D2, P, T), D2 < D.
clear(D, T) :- on(D, P, T), not blocked(D, T).

%% Top disk on a peg at time T
top(D, P, T) :- on(D, P, T), clear(D, T).

%% Empty peg: no disk on that peg at time T
empty(P, T) :- peg(P), time(T), not has_disk(P, T).
has_disk(P, T) :- on(_, P, T).

%% Choice of move at each step: at most one move per step
0 { move(D, From, To, S) : disk(D), peg(From), peg(To), From != To } 1 :- step(S).

%% Track which steps are actually used
used_step(S) :- move(_, _, _, S).

%% No gaps: if step S is used, all earlier steps must also be used
:- used_step(S), S > 1, not used_step(S-1).
:- step(S), not used_step(S), used_step(S+1).

%% Preconditions for a move at step S (state at time S-1)

%% 1. Disk must be on the source peg at time S-1
:- move(D, From, _, S), not on(D, From, S-1).

%% 2. Disk must be clear (top of its peg) at time S-1
:- move(D, _, _, S), not clear(D, S-1).

%% 3. Destination peg must have no smaller disk on top
%%    Either peg is empty, or top disk on peg is larger than moved disk
:- move(D, _, To, S), not empty(To, S-1), top(Top, To, S-1), Top < D.

%% Effects: state at time S

%% Moved disk arrives at destination
on(D, To, S) :- move(D, _, To, S).

%% A disk stays on its peg if not moved at step S
moved(D, S) :- move(D, _, _, S).
on(D, P, S) :- on(D, P, S-1), not moved(D, S), time(S).

%% Pilgrim's Journey: every disk must land on B and on C at least once
landed(D, b) :- move(D, _, b, _).
landed(D, c) :- move(D, _, c, _).

:- disk(D), not landed(D, b).
:- disk(D), not landed(D, c).

%% Goal: all disks on peg D at final time
final_step(S) :- used_step(S), not used_step(S+1).

%% All disks on peg D at the final step's time
all_on_d(S) :- disk(D), on(D, d, S).
goal(S) :- all_on_d(S).

:- final_step(S), not goal(S).

%% Minimize total number of moves
#minimize { 1, S : move(_, _, _, S) }.

%% Compute total moves count
total_moves(N) :- N = #count { S : move(_, _, _, S) }.

%% Output
#show move/4.
#show total_moves/1.