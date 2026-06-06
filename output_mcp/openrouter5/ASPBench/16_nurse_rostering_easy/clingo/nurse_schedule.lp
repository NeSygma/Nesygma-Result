%%% NURSE SCHEDULING PROBLEM %%%

% Domain definitions
nurse(1..4).
day(1..7).
shift(1..3).  % 1=morning, 2=evening, 3=night

% Coverage requirements
req(1, 2).  % morning: exactly 2 nurses
req(2, 1).  % evening: exactly 1 nurse
req(3, 1).  % night: exactly 1 nurse

% Weekend days
weekend(6;7).

% --- Hard Constraints ---

% 1. Coverage: exactly required number of nurses per shift per day
% Choice: assign nurses to shifts
{ assigned(N, D, S) : nurse(N) } :- day(D), shift(S).

% Exactly req(S) nurses per (D,S)
:- day(D), shift(S), req(S, R), 
   #count { N : assigned(N, D, S) } != R.

% 2. Single assignment: at most one shift per day per nurse
:- nurse(N), day(D), 
   #count { S : assigned(N, D, S) } > 1.

% 3. Rest period: cannot work night shift then morning shift next day
% Night shift is shift 3, morning shift is shift 1
:- nurse(N), day(D), D < 7,
   assigned(N, D, 3), assigned(N, D+1, 1).

% --- Soft Constraints (Violations) ---

% 4. Max consecutive days: each day beyond 3 consecutive adds 1 violation
% Count consecutive working days
work_day(N, D) :- assigned(N, D, _).

% Helper: consecutive sequences
% A run starts at day D if N works D but not D-1
run_start(N, D) :- work_day(N, D), not work_day(N, D-1), day(D).
% A run ends at day D if N works D but not D+1
run_end(N, D) :- work_day(N, D), not work_day(N, D+1), day(D).

% For each run, count days in the run
% run_length(N, Start, End, Len)
run_length(N, S, E, L) :- 
    run_start(N, S), run_end(N, E), 
    L = #count { D : work_day(N, D), D >= S, D <= E }.

% Violation: for each run, days beyond 3
violation_consec(N, S, E, V) :- 
    run_length(N, S, E, L), L > 3,
    V = L - 3.

total_violation_consec(V) :- 
    V = #sum { Vio, N, S, E : violation_consec(N, S, E, Vio) }.

% 5. Fair distribution: each nurse should work 6-8 shifts total
% Count total shifts per nurse
total_shifts(N, T) :- 
    nurse(N), 
    T = #count { D, S : assigned(N, D, S) }.

% Violation: below 6 or above 8
violation_fair(N, V) :- 
    total_shifts(N, T), T < 6, V = 6 - T.
violation_fair(N, V) :- 
    total_shifts(N, T), T > 8, V = T - 8.

total_violation_fair(V) :- 
    V = #sum { Vio, N : violation_fair(N, Vio) }.

% 6. Weekend coverage: at least 2 different nurses work weekend (days 6-7)
% Count distinct nurses working on weekend
weekend_nurse(N) :- assigned(N, D, _), weekend(D).

num_weekend_nurses(C) :- 
    C = #count { N : weekend_nurse(N) }.

violation_weekend(V) :- 
    num_weekend_nurses(C), C < 2, V = 1.
violation_weekend(0) :- 
    num_weekend_nurses(C), C >= 2.

% Total violations
total_violations(V) :- 
    total_violation_consec(V1), 
    total_violation_fair(V2), 
    violation_weekend(V3),
    V = V1 + V2 + V3.

% Minimize total violations
#minimize { V : total_violations(V) }.

% --- Output ---
% Show roster: assigned(N, D, S)
#show assigned/3.
#show total_violations/1.