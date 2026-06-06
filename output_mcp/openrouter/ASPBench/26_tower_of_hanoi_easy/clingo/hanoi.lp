% Domains
peg(a). peg(b). peg(c).

disk(1..4).

step(1..15).

% Initial state at time 0
at(4,a,0).
at(3,a,0).
at(2,a,0).
at(1,a,0).

% Helper: there exists a smaller disk on the same peg at a given step
smaller_exists(D,P,S) :- at(D,P,S), at(D2,P,S), D2 < D.

% Top disk definition
top(D,P,S) :- at(D,P,S), not smaller_exists(D,P,S).

% Move generation: exactly one move per step
1 { move(S,D,P1,P2) : disk(D), peg(P1), peg(P2), P1 != P2, top(D,P1,S-1), not smaller_exists(D,P2,S-1) } 1 :- step(S).

% Record which disk moves at which step
moved_at_step(D,S) :- move(S,D,_,_).

% State transition: place moved disk at destination
at(D,P,S) :- move(S,D,_,P).

% Persistence for disks not moved at this step
at(D,P,S) :- at(D,P,S-1), not moved_at_step(D,S), step(S).

% Each disk is on exactly one peg at each step
:- at(D,P1,S), at(D,P2,S), P1 != P2.

% Goal: all disks on peg c at step 15
:- disk(D), not at(D,c,15).

#show move/4.