% Size and time
size(5).
time(0..10).

% Initial state (given)
cell(1,1,0,0). cell(1,2,0,1). cell(1,3,0,0). cell(1,4,0,1). cell(1,5,0,0).
cell(2,1,0,1). cell(2,2,0,0). cell(2,3,0,1). cell(2,4,0,0). cell(2,5,0,1).
cell(3,1,0,0). cell(3,2,0,1). cell(3,3,0,0). cell(3,4,0,1). cell(3,5,0,0).
cell(4,1,0,1). cell(4,2,0,0). cell(4,3,0,1). cell(4,4,0,0). cell(4,5,0,1).
cell(5,1,0,0). cell(5,2,0,1). cell(5,3,0,0). cell(5,4,0,1). cell(5,5,0,0).

% Define neighbors
neighbor(X,Y,X1,Y1) :- size(S),
    X1 = X-1..X+1, Y1 = Y-1..Y+1,
    X1 >= 1, X1 <= S, Y1 >= 1, Y1 <= S,
    X1 != X, Y1 != Y.

% Count live neighbors for each cell at each time
live_neighbor(X,Y,T,X1,Y1) :- cell(X1,Y1,T,1), neighbor(X,Y,X1,Y1).

count_live_neighbors(X,Y,T,N) :- N = #count { X1,Y1 : live_neighbor(X,Y,T,X1,Y1) }.

% Evolution rules
% A live cell with 2 or 3 live neighbors survives
cell(X,Y,T+1,1) :- cell(X,Y,T,1), count_live_neighbors(X,Y,T,2).
cell(X,Y,T+1,1) :- cell(X,Y,T,1), count_live_neighbors(X,Y,T,3).

% A dead cell with exactly 3 live neighbors becomes alive
cell(X,Y,T+1,1) :- cell(X,Y,T,0), count_live_neighbors(X,Y,T,3).

% All other cells die or stay dead
cell(X,Y,T+1,0) :- cell(X,Y,T,1), count_live_neighbors(X,Y,T,N), N != 2, N != 3.
cell(X,Y,T+1,0) :- cell(X,Y,T,0), count_live_neighbors(X,Y,T,N), N != 3.

% Ensure all cells have a state at each time step
cell(X,Y,T,0) | cell(X,Y,T,1) :- size(S), X = 1..S, Y = 1..S, time(T), not cell(X,Y,T,0), not cell(X,Y,T,1).

% Helper to detect if states differ at two time steps
diff_state(T1,T2) :- cell(X,Y,T1,S1), cell(X,Y,T2,S2), S1 != S2.

% Cycle detection: Guess cycle_start and cycle_end
{ cycle_start(T) } :- time(T).
{ cycle_end(T) } :- time(T).

% Constraints for cycle detection
:- cycle_start(T1), cycle_end(T2), T1 >= T2.
:- cycle_start(T1), cycle_end(T2), T1 < T2,
    diff_state(T1,T2).  % States must be identical

% Ensure T1 is the first occurrence of that state
:- cycle_start(T1), time(T), T < T1, not diff_state(T, T1).

% Limit to simulation horizon
:- cycle_end(T2), T2 > 10.

% Define the period
period(P) :- cycle_start(T1), cycle_end(T2), P = T2 - T1.

% Define the states in the cycle
% The cycle includes states from T1 to T2-1
cycle_state(T,X,Y,S) :- cycle_start(T1), cycle_end(T2), T = T1..T2-1, cell(X,Y,T,S).

% Assign pattern ID
pattern_id(1).

% Output
#show pattern_id/1.
#show period/1.
#show cycle_state/4.