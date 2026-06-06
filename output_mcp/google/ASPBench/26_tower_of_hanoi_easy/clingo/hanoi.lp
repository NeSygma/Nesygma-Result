% --- Domain ---
disk(1..4).
peg("A"; "B"; "C").
time(0..15).

% --- Initial State ---
at(D, "A", 0) :- disk(D).

% --- Goal State ---
:- not at(D, "C", 15), disk(D).

% --- Actions ---
% Exactly one move per time step
1 { move(D, F, T, Time) : disk(D), peg(F), peg(T), F != T } 1 :- time(Time), Time < 15.

% --- Preconditions ---
% 1. Only top disk can be moved
is_top(D, P, Time) :- at(D, P, Time), not exists_smaller_on(D, P, Time).
exists_smaller_on(D, P, Time) :- at(D, P, Time), at(D2, P, Time), D2 < D.
:- move(D, F, T, Time), not is_top(D, F, Time).

% 2. Larger disk cannot be placed on smaller disk
% If we move D to T, there must be no smaller disk D2 already on T
:- move(D, F, T, Time), at(D2, T, Time), D2 < D.

% --- State Transitions ---
% Disk moves to new peg
at(D, T, Time+1) :- move(D, F, T, Time).
% Disk stays if not moved
at(D, P, Time+1) :- at(D, P, Time), not move(D, P, _, Time), time(Time+1).

% --- Integrity Constraints ---
% A disk cannot be at two pegs at once
:- at(D, P1, Time), at(D, P2, Time), P1 != P2.

% --- Output ---
% Map to required format
option(solution) :- at(D, "C", 15), disk(D).
#show move/4.
#show option/1.