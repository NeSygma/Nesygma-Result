%% Problem: Nurse Scheduling
%% Hard constraints: coverage, single assignment, rest period
%% Soft constraints: max consecutive days, fair distribution, weekend coverage

%% --- Domains ---
nurse(1..4).
day(1..7).
shift(1..3).

%% Shift requirements: morning=2, evening=1, night=1
requirement(1, 2).
requirement(2, 1).
requirement(3, 1).

%% --- Decision: assign nurse to day+shift ---
{ assigned(N, D, S) : nurse(N) } :- day(D), shift(S).

%% --- Hard Constraints ---

%% 1. Coverage: exactly the required number of nurses per shift per day
:- day(D), shift(S), requirement(S, R), 
   #count{ N : assigned(N, D, S) } != R.

%% 2. Single assignment: at most one shift per day per nurse
:- nurse(N), day(D), 
   #count{ S : assigned(N, D, S) } > 1.

%% 3. Rest period: night (shift 3) then next morning (shift 1) is forbidden
:- assigned(N, D, 3), assigned(N, D+1, 1), day(D), day(D+1).

%% --- Derived: nurse works on a particular day ---
works(N, D) :- assigned(N, D, S).

%% --- Soft Constraints (with violations counted) ---

%% 4. Max consecutive days: each day beyond 3 consecutive adds 1 violation
%% Day D is a 4th+ consecutive work day if N worked D, D-1, D-2, D-3
consec_violation(N, D) :- works(N, D), works(N, D-1), works(N, D-2), works(N, D-3), 
                          nurse(N), day(D), D-1 >= 1, D-2 >= 1, D-3 >= 1.

%% 5. Fair distribution: each nurse should work 6-8 shifts total
total_shifts(N, T) :- nurse(N), T = #count{ D, S : assigned(N, D, S) }.

fair_violation(N, V) :- nurse(N), total_shifts(N, T), T < 6, V = 6 - T.
fair_violation(N, V) :- nurse(N), total_shifts(N, T), T > 8, V = T - 8.

%% 6. Weekend coverage: at least 2 different nurses on days 6-7
weekend_worker(N) :- assigned(N, 6, S).
weekend_worker(N) :- assigned(N, 7, S).
weekend_count(C) :- C = #count{ N : weekend_worker(N) }.

weekend_violation(1) :- weekend_count(C), C < 2.

%% --- Violation count and minimization ---
#minimize { 1@1, N, D : consec_violation(N, D); 
            V@1, N : fair_violation(N, V); 
            1@1 : weekend_violation(1) }.

%% --- Output ---
#show assigned/3.
#show consec_violation/2.
#show fair_violation/2.
#show weekend_violation/1.
#show total_shifts/2.
#show weekend_count/1.