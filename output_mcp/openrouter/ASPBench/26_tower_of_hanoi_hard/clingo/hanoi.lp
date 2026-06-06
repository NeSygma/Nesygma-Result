% Tower of Hanoi with 4 disks, 4 pegs, mandatory visit B and C
% Horizon (allow up to 30 steps, optimizer will minimize moves)
#const max=30.

peg(a). peg(b). peg(c). peg(d).

disk(1..4).

% Possible moves (any disk can move from any peg to any other peg)
possible_move(Disk, From, To) :- disk(Disk), peg(From), peg(To), From != To.

% Time steps
time(0..max).

% Initial state at time 0
at(4,a,0). at(3,a,0). at(2,a,0). at(1,a,0).

% Define top disk on a peg at time T
smaller_on_same(Disk,Peg,T) :- at(Disk,Peg,T), at(Smaller,Peg,T), Smaller < Disk.

top(Disk,Peg,T) :- at(Disk,Peg,T), not smaller_on_same(Disk,Peg,T).

% Move choice: at most one move per time step (time>0)
{ move(T, Disk, From, To) : possible_move(Disk, From, To) } 0..1 :- time(T), T > 0.

% Preconditions for a move (ensure T-1 is within time domain)
:- move(T, Disk, From, _), not at(Disk, From, T-1), time(T), time(T-1).
:- move(T, Disk, From, _), not top(Disk, From, T-1), time(T), time(T-1).
% Cannot place larger disk onto smaller one at destination
:- move(T, Disk, _, To), at(Smaller, To, T-1), Smaller < Disk, time(T), time(T-1).

% State transition
% If a disk is moved, its new location is the destination
at(Disk, To, T) :- move(T, Disk, _, To), time(T).
% Disks not moved stay where they were
at(Disk, Peg, T) :- at(Disk, Peg, T-1), not move(T, Disk, _, _), time(T), time(T-1).

% Journey constraints: each disk must visit B and C at least once (as destination)
visitedB(Disk) :- move(_, Disk, _, b).
visitedC(Disk) :- move(_, Disk, _, c).
:- disk(Disk), not visitedB(Disk).
:- disk(Disk), not visitedC(Disk).

% Goal: all disks on peg d at final time max
:- disk(Disk), not at(Disk, d, max).
% No disks on other pegs at final time
:- at(Disk, Peg, max), Peg != d.

% Optimization: minimize number of moves
#minimize { 1,T : move(T,_,_,_) }.

% Show the moves
#show move/4.
% Show total number of moves
total_moves(N) :- N = #count { T : move(T,_,_,_) }.
#show total_moves/1.