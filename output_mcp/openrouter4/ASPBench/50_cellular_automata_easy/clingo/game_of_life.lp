% --- Domain Definitions ---
row(0..4).
col(0..4).
time(0..10).

% --- Initial State (Time 0) ---
% Checkerboard pattern from the problem instance
cell_alive(0,1,0). cell_alive(0,3,0).
cell_alive(1,0,0). cell_alive(1,2,0). cell_alive(1,4,0).
cell_alive(2,1,0). cell_alive(2,3,0).
cell_alive(3,0,0). cell_alive(3,2,0). cell_alive(3,4,0).
cell_alive(4,1,0). cell_alive(4,3,0).

% --- Neighbor Relation (8 directions) ---
neighbor(X, Y, X-1, Y-1) :- row(X), col(Y), X-1 >= 0, Y-1 >= 0.
neighbor(X, Y, X-1, Y)   :- row(X), col(Y), X-1 >= 0.
neighbor(X, Y, X-1, Y+1) :- row(X), col(Y), X-1 >= 0, Y+1 <= 4.
neighbor(X, Y, X, Y-1)   :- row(X), col(Y), Y-1 >= 0.
neighbor(X, Y, X, Y+1)   :- row(X), col(Y), Y+1 <= 4.
neighbor(X, Y, X+1, Y-1) :- row(X), col(Y), X+1 <= 4, Y-1 >= 0.
neighbor(X, Y, X+1, Y)   :- row(X), col(Y), X+1 <= 4.
neighbor(X, Y, X+1, Y+1) :- row(X), col(Y), X+1 <= 4, Y+1 <= 4.

% --- Neighbor Count ---
neighbor_count(X, Y, T, N) :- 
    row(X), col(Y), time(T),
    N = #count{Xn, Yn : neighbor(X, Y, Xn, Yn), cell_alive(Xn, Yn, T)}.

% --- Conway's Game of Life Evolution Rules ---
% Survival: live cell with 2 or 3 neighbors stays alive
cell_alive(X, Y, T+1) :- 
    cell_alive(X, Y, T), 
    neighbor_count(X, Y, T, N), 
    N >= 2, N <= 3, 
    time(T), time(T+1).

% Reproduction: dead cell with exactly 3 neighbors becomes alive
cell_alive(X, Y, T+1) :- 
    not cell_alive(X, Y, T), 
    neighbor_count(X, Y, T, N), 
    N = 3, 
    time(T), time(T+1).

% --- Cycle Detection ---
% Detect mismatches between configurations at two time points
mismatch(T1, T2, X, Y) :- 
    row(X), col(Y), time(T1), time(T2),
    cell_alive(X, Y, T1), not cell_alive(X, Y, T2).
mismatch(T1, T2, X, Y) :- 
    row(X), col(Y), time(T1), time(T2),
    not cell_alive(X, Y, T1), cell_alive(X, Y, T2).

% True if any mismatch exists between T1 and T2
has_mismatch(T1, T2) :- mismatch(T1, T2, _, _).

% Two time points have equal grid configurations
grid_equal(T1, T2) :- 
    time(T1), time(T2), T1 < T2, 
    not has_mismatch(T1, T2).

% Time T2 where a previous state repeats
repeat_time(T2) :- 
    time(T2), 
    grid_equal(T1, T2), T1 < T2.

% Helper: T2 has an earlier repeat time
has_earlier_repeat(T2) :- repeat_time(T3), time(T3), T3 < T2, time(T2).

% First (smallest) time at which a repeat occurs
first_repeat(T2) :- 
    repeat_time(T2), 
    not has_earlier_repeat(T2).

% Helper: T1 has an earlier time that also equals T2
has_earlier_equal(T1, T2) :- grid_equal(T3, T2), time(T3), T3 < T1, time(T1).

% Start of the cycle: smallest T1 such that grid_equal(T1, T2)
cycle_start(T1) :- 
    first_repeat(T2), 
    grid_equal(T1, T2), 
    not has_earlier_equal(T1, T2).

% Period of the cycle
period(P) :- 
    cycle_start(T1), first_repeat(T2), 
    P = T2 - T1.

% Pattern ID (always 1 for the first stable pattern)
pattern_id(1).

% --- Extract all states in the cycle ---
% State in cycle: all states from cycle_start up to (but not including) first_repeat
state_in_cycle(X, Y, T_offset, 1) :- 
    cycle_start(T1), first_repeat(T2),
    time(T),
    T1 <= T, T < T2,
    T_offset = T - T1,
    row(X), col(Y),
    cell_alive(X, Y, T).

state_in_cycle(X, Y, T_offset, 0) :- 
    cycle_start(T1), first_repeat(T2),
    time(T),
    T1 <= T, T < T2,
    T_offset = T - T1,
    row(X), col(Y),
    not cell_alive(X, Y, T).

% --- Output Directives ---
#show pattern_id/1.
#show period/1.
#show state_in_cycle/4.