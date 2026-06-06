% --- Domain Definitions ---
nurse(1..5).
day(1..10).
shift(1..3).

% --- Decision: Assign nurses to shifts ---
% For each day and shift, assign the required number of nurses
2 { assigned(N, D, 1) : nurse(N) } 2 :- day(D).
1 { assigned(N, D, 2) : nurse(N) } 1 :- day(D).
1 { assigned(N, D, 3) : nurse(N) } 1 :- day(D).

% --- Constraint 2: At most one shift per nurse per day ---
:- nurse(N), day(D), shift(S1), shift(S2), S1 < S2,
   assigned(N, D, S1), assigned(N, D, S2).

% --- Constraint 3: Night shift followed by morning shift is forbidden ---
:- nurse(N), day(D), D < 10,
   assigned(N, D, 3), assigned(N, D+1, 1).

% --- Output: Show the roster ---
#show assigned/3.