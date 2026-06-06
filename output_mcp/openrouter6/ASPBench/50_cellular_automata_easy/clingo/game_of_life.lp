% Conway's Game of Life on 5x5 grid, detect stable pattern within 10 steps

% Domain
cell_x(1..5).
cell_y(1..5).
time(0..10).

% Initial configuration (0 = dead, 1 = alive)
initial(1,1,0). initial(1,2,1). initial(1,3,0). initial(1,4,1). initial(1,5,0).
initial(2,1,1). initial(2,2,0). initial(2,3,1). initial(2,4,0). initial(2,5,1).
initial(3,1,0). initial(3,2,1). initial(3,3,0). initial(3,4,1). initial(3,5,0).
initial(4,1,1). initial(4,2,0). initial(4,3,1). initial(4,4,0). initial(4,5,1).
initial(5,1,0). initial(5,2,1). initial(5,3,0). initial(5,4,1). initial(5,5,0).

% Cell alive at time 0
cell(X,Y,0) :- initial(X,Y,1).

% Neighbor offsets (8 directions)
offset(-1,-1). offset(-1,0). offset(-1,1).
offset(0,-1).           offset(0,1).
offset(1,-1).  offset(1,0).  offset(1,1).

% Neighbor count for each cell at each time
neighbor_count(X,Y,T,N) :-
    cell_x(X), cell_y(Y), time(T),
    N = #count { X2, Y2 : offset(DX,DY), X2 = X+DX, Y2 = Y+DY,
                 cell_x(X2), cell_y(Y2), cell(X2,Y2,T) }.

% Evolution rules (Conway's Game of Life)
cell(X,Y,T+1) :-
    cell_x(X), cell_y(Y), time(T), time(T+1),
    cell(X,Y,T), neighbor_count(X,Y,T,N), N >= 2, N <= 3.

cell(X,Y,T+1) :-
    cell_x(X), cell_y(Y), time(T), time(T+1),
    not cell(X,Y,T), neighbor_count(X,Y,T,N), N == 3.

% State difference predicate
state_diff(S,T) :-
    cell_x(X), cell_y(Y),
    cell(X,Y,S), not cell(X,Y,T).

state_diff(S,T) :-
    cell_x(X), cell_y(Y),
    not cell(X,Y,S), cell(X,Y,T).

% State equality (two states are identical)
equal_state(S,T) :- time(S), time(T), S < T, not state_diff(S,T).

% First cycle detection: find the earliest repetition
first_cycle_end(T) :-
    equal_state(S,T), S < T,
    not ( equal_state(S2,T2), T2 < T ).

first_cycle_start(S) :-
    first_cycle_end(T), equal_state(S,T).

% Period of the cycle
period(P) :- first_cycle_start(S), first_cycle_end(T), P = T - S.

% Pattern ID (only one pattern is output)
pattern_id(1).

% Map pattern state indices to actual time steps
pattern_time(1, StateIndex, Time) :-
    pattern_id(1), first_cycle_start(S), first_cycle_end(T), period(P),
    StateIndex = 0..P-1, Time = S + StateIndex.

% Pattern cell values (1 = alive, 0 = dead)
pattern_cell(1, StateIndex, X, Y, 1) :-
    pattern_time(1, StateIndex, Time),
    cell(X,Y,Time).

pattern_cell(1, StateIndex, X, Y, 0) :-
    pattern_time(1, StateIndex, Time),
    not cell(X,Y,Time).

% Output the pattern
pattern(1, P) :- period(P).

% Show directives
#show pattern/2.
#show pattern_cell/5.