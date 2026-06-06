% Conway's Game of Life with Cycle Detection
% 5x5 grid, simulate up to 10 time steps

% Domain declarations
cell(0..4, 0..4).
time(0..10).

% Initial configuration (time 0)
alive(0,1,0). alive(0,3,0).
alive(1,0,0). alive(1,2,0). alive(1,4,0).
alive(2,1,0). alive(2,3,0).
alive(3,0,0). alive(3,2,0). alive(3,4,0).
alive(4,1,0). alive(4,3,0).

% Neighbor relationships (8 directions)
neighbor(R1, C1, R2, C2) :- 
    cell(R1, C1), cell(R2, C2),
    R1 != R2, C1 != C2,
    R2 >= R1-1, R2 <= R1+1,
    C2 >= C1-1, C2 <= C1+1.

% Count alive neighbors for each cell at each time
neighbor_count(R, C, T, N) :-
    cell(R, C), time(T),
    N = #count{ R2, C2 : neighbor(R, C, R2, C2), alive(R2, C2, T) }.

% Evolution rules
% Rule 1: Living cell with < 2 neighbors dies (underpopulation)
alive(R, C, T+1) :- cell(R, C), time(T), T < 10,
    alive(R, C, T), neighbor_count(R, C, T, N), N >= 2, N <= 3.

% Rule 4: Dead cell with exactly 3 neighbors becomes alive (reproduction)
alive(R, C, T+1) :- cell(R, C), time(T), T < 10,
    not alive(R, C, T), neighbor_count(R, C, T, 3).

% State representation: encode grid as a number for comparison
% For 5x5 grid, we can encode as a 25-bit number
state_id(T, S) :-
    time(T),
    S = #sum{ 2^(R*5+C), R, C : alive(R, C, T) }.

% Cycle detection: find first repetition
% For each pair of times T1 < T2, if states are equal, we have a cycle
cycle_start(T1) :-
    time(T1), time(T2), T1 < T2,
    state_id(T1, S), state_id(T2, S),
    not earlier_cycle(T1).

% Helper: T1 is not the start of an earlier cycle
earlier_cycle(T1) :-
    time(T1), time(T2), T1 < T2,
    state_id(T1, S), state_id(T2, S),
    time(T3), T3 < T1,
    state_id(T3, S3), state_id(T4, S4), T3 < T4, S3 = S4.

% Period of the cycle
cycle_period(P) :-
    cycle_start(T1),
    P = #min{ T2 - T1 : time(T2), T2 > T1, 
              state_id(T1, S), state_id(T2, S) }.

% Extract states in the cycle
% For pattern 1 (the first detected cycle)
pattern_id(1).
pattern_period(1, P) :- cycle_period(P).

% States in the cycle: from T1 to T1+P-1
pattern_state(1, S) :-
    pattern_id(1), cycle_start(T1), cycle_period(P),
    time(T), T >= T1, T < T1 + P,
    state_id(T, S).

% Show the results
#show pattern_id/1.
#show cycle_start/1.
#show cycle_period/1.
#show pattern_state/2.
#show pattern_period/2.

% Also show the grid states for verification
#show alive/3.