% --- Domain and Initial State ---
x(1..5). y(1..5). time(0..10).

% Initial grid configuration
cell(1,1,0,0).
cell(1,2,1,0).
cell(1,3,0,0).
cell(1,4,1,0).
cell(1,5,0,0).

cell(2,1,1,0).
cell(2,2,0,0).
cell(2,3,1,0).
cell(2,4,0,0).
cell(2,5,1,0).

cell(3,1,0,0).
cell(3,2,1,0).
cell(3,3,0,0).
cell(3,4,1,0).
cell(3,5,0,0).

cell(4,1,1,0).
cell(4,2,0,0).
cell(4,3,1,0).
cell(4,4,0,0).
cell(4,5,1,0).

cell(5,1,0,0).
cell(5,2,1,0).
cell(5,3,0,0).
cell(5,4,1,0).
cell(5,5,0,0).

% Define neighbors for each cell
neighbor(X, Y, Xn, Yn) :-
    x(X), y(Y), x(Xn), y(Yn),
    (Xn = X-1; Xn = X; Xn = X+1),
    (Yn = Y-1; Yn = Y; Yn = Y+1),
    (Xn != X; Yn != Y),
    Xn >= 1, Xn <= 5, Yn >= 1, Yn <= 5.

% Count live neighbors for cell (X,Y) at time T
live_neighbors(X, Y, T, N) :-
    x(X), y(Y), time(T),
    N = #count { Xn, Yn : neighbor(X, Y, Xn, Yn), cell(Xn, Yn, T, 1) }.

% Derive next state for each cell
cell(X, Y, T+1, 1) :-
    cell(X, Y, T, 1),
    live_neighbors(X, Y, T, N),
    N = 2.

cell(X, Y, T+1, 1) :-
    cell(X, Y, T, 1),
    live_neighbors(X, Y, T, N),
    N = 3.

cell(X, Y, T+1, 0) :-
    cell(X, Y, T, 1),
    live_neighbors(X, Y, T, N),
    N < 2.

cell(X, Y, T+1, 0) :-
    cell(X, Y, T, 1),
    live_neighbors(X, Y, T, N),
    N > 3.

cell(X, Y, T+1, 1) :-
    cell(X, Y, T, 0),
    live_neighbors(X, Y, T, N),
    N = 3.

cell(X, Y, T+1, 0) :-
    cell(X, Y, T, 0),
    live_neighbors(X, Y, T, N),
    N != 3.

% Detect when a state repeats
state_repeats(T1, T2) :-
    time(T1), time(T2),
    T1 < T2,
    cell(X, Y, T1, V) : cell(X, Y, T2, V) : x(X), y(Y), V = 0..1.

% Find the first cycle start
cycle_start(T) :-
    state_repeats(T, T2),
    not (state_repeats(Tp, T2), Tp < T).

% Find the period of the cycle starting at T
cycle_period(T, P) :-
    cycle_start(T),
    state_repeats(T, T2),
    P = T2 - T.

% Extract all states in the cycle
% Helper to collect states in the cycle
cycle_state(T, T, X, Y, V) :-
    cycle_start(T),
    cell(X, Y, T, V).

cycle_state(T, Tp, X, Y, V) :-
    cycle_period(T, P),
    Tp = T + 1,
    Tp < T + P,
    cell(X, Y, Tp, V).

cycle_state(T, Tp, X, Y, V) :-
    cycle_period(T, P),
    Tp > T + 1,
    Tp < T + P,
    cycle_state(T, Tp-1, X, Y, _),
    cell(X, Y, Tp, V).

% Map to stable_pattern/3
pattern_id(1).
stable_pattern(PatternID, Period, States) :-
    pattern_id(PatternID),
    cycle_start(T),
    cycle_period(T, Period),
    States = t(T).

#show stable_pattern/3.