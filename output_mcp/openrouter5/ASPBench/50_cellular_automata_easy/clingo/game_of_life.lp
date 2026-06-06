% Conway's Game of Life - Stable Pattern Detection
% 5x5 grid, simulate up to 10 time steps

% Define the grid dimensions
row(0..4).
col(0..4).

% Define time steps (0 = initial, up to 10)
time(0..10).

% Initial alive cells (where value = 1)
alive(0,0,0). alive(0,2,0). alive(0,4,0).
alive(1,1,0). alive(1,3,0).
alive(2,0,0). alive(2,2,0). alive(2,4,0).
alive(3,1,0). alive(3,3,0).
alive(4,0,0). alive(4,2,0). alive(4,4,0).

% Dead cells at time 0 are those not alive
dead(R,C,0) :- row(R), col(C), not alive(R,C,0).

% Neighbor positions: 8 directions
neighbor_offset(-1,-1). neighbor_offset(-1,0). neighbor_offset(-1,1).
neighbor_offset(0,-1). neighbor_offset(0,1).
neighbor_offset(1,-1). neighbor_offset(1,0). neighbor_offset(1,1).

% Count live neighbors for each cell at each time
% Use a helper predicate to count neighbors
live_neighbor(R,C,T,DR,DC) :- 
    row(R), col(C), time(T),
    neighbor_offset(DR,DC),
    row(R+DR), col(C+DC), 
    alive(R+DR, C+DC, T).

% neighbor_count(R,C,T,N) - N is the number of live neighbors
neighbor_count(R,C,T,N) :- 
    row(R), col(C), time(T),
    N = #count{DR,DC : live_neighbor(R,C,T,DR,DC)}.

% Evolution rules for next generation

% Survival: alive cell with 2 or 3 neighbors stays alive
alive(R,C,T+1) :- alive(R,C,T), neighbor_count(R,C,T,N), N >= 2, N <= 3, time(T+1).

% Death by underpopulation: alive cell with < 2 neighbors dies
dead(R,C,T+1) :- alive(R,C,T), neighbor_count(R,C,T,N), N < 2, time(T+1).

% Death by overpopulation: alive cell with > 3 neighbors dies
dead(R,C,T+1) :- alive(R,C,T), neighbor_count(R,C,T,N), N > 3, time(T+1).

% Reproduction: dead cell with exactly 3 neighbors becomes alive
alive(R,C,T+1) :- dead(R,C,T), neighbor_count(R,C,T,N), N == 3, time(T+1).

% Dead cells at T+1 that are not alive at T+1
dead(R,C,T+1) :- row(R), col(C), time(T+1), not alive(R,C,T+1).

% Each cell is either alive or dead at each time (exclusivity)
:- alive(R,C,T), dead(R,C,T).

% Cycle detection: find when a state repeats
% Two times T1 < T2 have the same state if the same cells are alive

% Helper: for each pair of times, check if alive sets match
% First, count how many cells differ between T1 and T2
diff_count(T1,T2,N) :- 
    time(T1), time(T2), T1 < T2,
    N = #count{R,C : alive(R,C,T1), not alive(R,C,T2); R,C : alive(R,C,T2), not alive(R,C,T1)}.

% same_state when no cells differ
same_state(T1,T2) :- diff_count(T1,T2,0), time(T1), time(T2), T1 < T2.

% Detect the first cycle: find the earliest T1 and T2 where T1 < T2 and same_state
% cycle_start(T1) means T1 is the first time that starts a cycle
cycle_start(T1) :- 
    time(T1), 
    same_state(T1, T2),
    not time(T0), T0 < T1, same_state(T0, _).

% cycle_end(T2) is the matching time for the cycle start
cycle_end(T2) :- 
    cycle_start(T1), 
    same_state(T1, T2),
    not time(T3), T3 < T2, T3 > T1, same_state(T1, T3).

% period = T2 - T1
period(P) :- cycle_start(T1), cycle_end(T2), P = T2 - T1.

% States in the cycle: all times from T1 to T2-1
in_cycle(T) :- cycle_start(T1), cycle_end(T2), time(T), T >= T1, T < T2.

% Output the pattern
% pattern_id is always 1 for the first stable pattern
pattern_id(1).

% Show results
#show pattern_id/1.
#show period/1.
#show in_cycle/1.
#show alive/3.