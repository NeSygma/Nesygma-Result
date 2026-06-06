% Constants
disk(1..4).
peg(a;b;c;d).

% Time horizon - we'll search up to a reasonable bound
% The expected optimal is 19 moves, so let's use 30 as a safe upper bound
time(0..30).

% Initial state: at time 0, all disks are on peg A in order 4,3,2,1 (4 at bottom)
% We represent this as facts
at(1, a, 0).
at(2, a, 0).
at(3, a, 0).
at(4, a, 0).

% Choice rule: generate possible moves
% A move consists of moving a disk from one peg to another
{ move(T, D, From, To) : disk(D), peg(From), peg(To), From != To } 1 :- time(T), T > 0.

% The top disk is the one with no smaller disk above it on the same peg
top_disk(D, P, T) :- at(D, P, T),
                     disk(D),
                     peg(P),
                     time(T),
                     not at(D2, P, T) : disk(D2), D2 < D.

% A move is valid only if it moves the top disk
:- move(T, D, From, To), not top_disk(D, From, T-1).

% Constraint: no larger disk on smaller disk
% After a move, the destination peg must have disks in decreasing order
:- move(T, D, From, To),
   at(D2, To, T),
   disk(D2),
   disk(D),
   D2 < D.

% Frame axioms: state persists unless changed by a move
at(D, P, T) :- at(D, P, T-1), time(T), not move(T, D, P, _), not move(T, D, _, P).

% Effect of move: update the state
at(D, To, T) :- move(T, D, _, To), time(T).
:- move(T, D, From, To), at(D, From, T).

% Pilgrim's journey: each disk must be moved to B at least once and to C at least once
landed_on_b(D) :- move(T, D, _, b), disk(D), time(T).
landed_on_c(D) :- move(T, D, _, c), disk(D), time(T).

% Every disk must land on B and C at least once
:- disk(D), not landed_on_b(D).
:- disk(D), not landed_on_c(D).

% Goal state: all disks on peg D at the final time step
:- disk(D), not at(D, d, 30).

% Optimization: minimize the number of moves
#minimize { T@1 : move(T, _, _, _) }.

% Show the solution
#show move/4.