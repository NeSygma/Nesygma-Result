%% Tower of Hanoi with 4 disks, 4 pegs, and Pilgrim's Journey constraint
%% Goal: Minimize moves while ensuring every disk visits pegs B and C at least once.

%% --- Domain Definitions ---
disk(1..4).
peg(a;b;c;d).

%% Time horizon - expected optimal is 19 moves
time(0..19).

%% --- Initial State ---
%% on(Disk, Peg, Time): Disk is on Peg at Time
on(1, a, 0).
on(2, a, 0).
on(3, a, 0).
on(4, a, 0).

%% --- Goal: all disks on peg D at some time ---
goal :- on(1, d, 19), on(2, d, 19), on(3, d, 19), on(4, d, 19).
:- not goal.

%% --- Movement: exactly one move per time step ---
{ move(Disk, From, To, T) : disk(Disk), peg(From), peg(To), From != To } 1 :- time(T), T < 19.

%% Exactly one move per step
:- time(T), T < 19, #count{D,F,T2 : move(D,F,T2,T)} != 1.

%% --- Preconditions ---

%% 1. A disk can only move if it's the top disk on its peg.
%% A disk is top if no smaller disk is on the same peg
top(Disk, T) :- disk(Disk), time(T), 
                not (disk(D2), D2 < Disk, on(D2, P, T), on(Disk, P, T)).

%% Moved disk must be top on its source peg
:- move(Disk, From, _, T), not top(Disk, T).
:- move(Disk, From, _, T), not on(Disk, From, T).

%% 2. Larger disk cannot be placed on smaller disk.
:- move(Disk, _, To, T), 
   disk(TopDisk), TopDisk < Disk,
   on(TopDisk, To, T),
   top(TopDisk, T).

%% --- Effects ---

%% Disk moves to new peg
on(Disk, To, T+1) :- move(Disk, _, To, T), time(T+1).

%% Disk leaves old peg
:- move(Disk, From, _, T), on(Disk, From, T+1).

%% Other disks stay where they are (frame axiom)
on(Disk, Peg, T+1) :- on(Disk, Peg, T), time(T+1), not move(Disk, _, _, T).

%% --- Pilgrim's Journey Constraint ---
%% Every disk must land on peg B at least once AND on peg C at least once.
visited_peg(Disk, Peg) :- move(Disk, _, Peg, _).

:- disk(D), not visited_peg(D, b).
:- disk(D), not visited_peg(D, c).

%% --- Minimize total moves ---
#minimize { T, D, F, T2 : move(D, F, T2, T) }.

%% --- Show results ---
#show move/4.