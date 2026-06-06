% Grid dimensions
row(1..5).
col(1..5).
time(0..10).

% Initial state
init(1, 2). init(1, 4).
init(2, 1). init(2, 3). init(2, 5).
init(3, 2). init(3, 4).
init(4, 1). init(4, 3). init(4, 5).
init(5, 2). init(5, 4).

state(R, C, 0) :- init(R, C).
dead(R, C, 0) :- row(R), col(C), not init(R, C).

% Neighbor definition
neighbor(R, C, NR, NC) :- row(R), col(C), row(NR), col(NC),
    R-NR >= -1, R-NR <= 1, C-NC >= -1, C-NC <= 1, (R, C) != (NR, NC).

% Count neighbors
count_neighbors(R, C, T, N) :- row(R), col(C), time(T),
    N = #count { NR, NC : neighbor(R, C, NR, NC), state(NR, NC, T) }.

% Evolution rules
state(R, C, T+1) :- row(R), col(C), time(T), T < 10,
    state(R, C, T), count_neighbors(R, C, T, N), N >= 2, N <= 3.
state(R, C, T+1) :- row(R), col(C), time(T), T < 10,
    dead(R, C, T), count_neighbors(R, C, T, N), N = 3.

dead(R, C, T+1) :- row(R), col(C), time(T), T < 10,
    state(R, C, T), count_neighbors(R, C, T, N), N < 2.
dead(R, C, T+1) :- row(R), col(C), time(T), T < 10,
    state(R, C, T), count_neighbors(R, C, T, N), N > 3.
dead(R, C, T+1) :- row(R), col(C), time(T), T < 10,
    dead(R, C, T), count_neighbors(R, C, T, N), N != 3.

% Cycle detection
diff(T1, T2) :- time(T1), time(T2), T1 < T2, row(R), col(C),
    state(R, C, T1), dead(R, C, T2).
diff(T1, T2) :- time(T1), time(T2), T1 < T2, row(R), col(C),
    dead(R, C, T1), state(R, C, T2).
same_state(T1, T2) :- time(T1), time(T2), T1 < T2, not diff(T1, T2).

% Find the first cycle
first_cycle(T1, T2) :- same_state(T1, T2),
    not same_state_earlier(T1, T2).
same_state_earlier(T1, T2) :- same_state(T1, T2), same_state(T1, T_prev), T_prev < T2.

% Output
period(P) :- first_cycle(T1, T2), P = T2 - T1.
#show period/1.
#show first_cycle/2.