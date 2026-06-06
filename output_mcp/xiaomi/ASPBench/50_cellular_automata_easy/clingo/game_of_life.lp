% Grid dimensions
pos(0..4).

% Grid cells
cell(X,Y) :- pos(X), pos(Y).

% Initial state (from the given configuration)
% Row 0: 0 1 0 1 0
alive(1,0,0). alive(3,0,0).
% Row 1: 1 0 1 0 1
alive(0,1,0). alive(2,1,0). alive(4,1,0).
% Row 2: 0 1 0 1 0
alive(1,2,0). alive(3,2,0).
% Row 3: 1 0 1 0 1
alive(0,3,0). alive(2,3,0). alive(4,3,0).
% Row 4: 0 1 0 1 0
alive(1,4,0). alive(3,4,0).

% Time steps (simulate up to 10 generations)
time(0..10).

% Neighbor relationships (8-connected, with wrapping for edge cells)
% Right
neighbor(X,Y,XR,Y) :- cell(X,Y), pos(XR), XR = (X+1)\5.
% Left
neighbor(X,Y,XL,Y) :- cell(X,Y), pos(XL), XL = (X-1+5)\5.
% Down
neighbor(X,Y,X,YD) :- cell(X,Y), pos(YD), YD = (Y+1)\5.
% Up
neighbor(X,Y,X,YU) :- cell(X,Y), pos(YU), YU = (Y-1+5)\5.
% Diagonal down-right
neighbor(X,Y,XR,YD) :- cell(X,Y), pos(XR), pos(YD), XR = (X+1)\5, YD = (Y+1)\5.
% Diagonal down-left
neighbor(X,Y,XL,YD) :- cell(X,Y), pos(XL), pos(YD), XL = (X-1+5)\5, YD = (Y+1)\5.
% Diagonal up-right
neighbor(X,Y,XR,YU) :- cell(X,Y), pos(XR), pos(YU), XR = (X+1)\5, YU = (Y-1+5)\5.
% Diagonal up-left
neighbor(X,Y,XL,YU) :- cell(X,Y), pos(XL), pos(YU), XL = (X-1+5)\5, YU = (Y-1+5)\5.

% Count live neighbors at each time step
live_count(X,Y,T,N) :- cell(X,Y), time(T), 
    N = #count { NX,NY : neighbor(X,Y,NX,NY), alive(NX,NY,T) }.

% Game of Life rules for T+1
% Dead cell with exactly 3 neighbors becomes alive
alive(X,Y,T+1) :- cell(X,Y), time(T), time(T+1), not alive(X,Y,T), live_count(X,Y,T,3).

% Living cell with 2-3 neighbors survives
alive(X,Y,T+1) :- cell(X,Y), time(T), time(T+1), alive(X,Y,T), live_count(X,Y,T,2).
alive(X,Y,T+1) :- cell(X,Y), time(T), time(T+1), alive(X,Y,T), live_count(X,Y,T,3).

% Cells that don't meet survival/reproduction conditions die
% (handled by CWA - if not derived alive, it's dead)

% Cycle detection: find when a state repeats
% Two states are equal if all cells have same alive/dead status
mismatch(T1,T2) :- time(T1), time(T2), T1 < T2, cell(X,Y),
    alive(X,Y,T1), not alive(X,Y,T2).
mismatch(T1,T2) :- time(T1), time(T2), T1 < T2, cell(X,Y),
    not alive(X,Y,T1), alive(X,Y,T2).

state_match(T1,T2) :- time(T1), time(T2), T1 < T2,
    not mismatch(T1,T2).

% Find the first cycle (earliest T2 where state matches some earlier T1)
first_cycle_end(T2) :- state_match(_,T2),
    not state_match(_,T2_) : T2_ < T2, state_match(_,T2_).

% Get the corresponding start (earliest T1 that matches T2)
cycle_start(T1) :- first_cycle_end(T2), state_match(T1,T2),
    not state_match(T1_,T2) : T1_ < T1, state_match(T1_,T2).

% Period of the cycle
period(P) :- first_cycle_end(T2), cycle_start(T1), P = T2 - T1.

% States in the cycle (from start to end-1)
in_cycle(T) :- time(T), cycle_start(T1), first_cycle_end(T2), T1 <= T, T < T2.

% Output: show the cycle information
#show period/1.
#show cycle_start/1.
#show first_cycle_end/1.
#show in_cycle/1.
#show alive/3.