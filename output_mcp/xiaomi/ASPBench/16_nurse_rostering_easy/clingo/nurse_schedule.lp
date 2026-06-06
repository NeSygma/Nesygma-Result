% ===== DOMAIN DEFINITIONS =====
nurse(1..4).
day(1..7).
shift(1..3).  % 1=morning, 2=evening, 3=night

% Weekend days
weekend(6).
weekend(7).

% ===== COVERAGE REQUIREMENTS =====
% Morning (shift 1): exactly 2 nurses
% Evening (shift 2): exactly 1 nurse  
% Night (shift 3): exactly 1 nurse
required(1, 2).  % shift 1 needs 2
required(2, 1).  % shift 2 needs 1
required(3, 1).  % shift 3 needs 1

% ===== DECISION VARIABLES =====
% Each nurse can be assigned to at most one shift per day
{ assigned(N, D, S) : shift(S) } 1 :- nurse(N), day(D).

% ===== HARD CONSTRAINT 1: COVERAGE REQUIREMENT =====
% Each shift must have exactly the required number of nurses
:- day(D), shift(S), required(S, R), #count{N : assigned(N, D, S)} != R.

% ===== HARD CONSTRAINT 2: SINGLE ASSIGNMENT =====
% Already enforced by the choice rule above (at most 1 shift per day)

% ===== HARD CONSTRAINT 3: REST PERIOD =====
% Cannot work night shift (3) on day D and morning shift (1) on day D+1
:- assigned(N, D, 3), assigned(N, D+1, 1), day(D), day(D+1).

% ===== HELPER: WORKED ON DAY =====
worked(N, D) :- assigned(N, D, _).

% ===== SOFT CONSTRAINT 4: MAX CONSECUTIVE DAYS =====
% Count consecutive work days for each nurse
% A nurse works consecutively from day D if they work D and D-1
consecutive(N, D) :- worked(N, D), worked(N, D-1), day(D), day(D-1).

% Count consecutive streaks: if consecutive at D, streak continues
streak(N, D, 1) :- worked(N, D), not worked(N, D-1), day(D).
streak(N, D, C) :- consecutive(N, D), streak(N, D-1, C-1), C > 1, day(D), day(D-1).

% Violation: each day beyond 3 consecutive adds 1 violation
violation_consecutive(N, V) :- 
    nurse(N), 
    V = #sum{C-3 : streak(N, D, C), C > 3}.

% ===== SOFT CONSTRAINT 5: FAIR DISTRIBUTION =====
% Each nurse should work 6-8 shifts total
total_shifts(N, C) :- nurse(N), C = #count{D, S : assigned(N, D, S)}.

% Violation: each shift below 6 or above 8 adds 1 violation
violation_fair(N, V) :- 
    nurse(N), 
    total_shifts(N, C),
    C >= 6, C <= 8,
    V = 0.
violation_fair(N, V) :- 
    nurse(N), 
    total_shifts(N, C),
    C < 6,
    V = 6 - C.
violation_fair(N, V) :- 
    nurse(N), 
    total_shifts(N, C),
    C > 8,
    V = C - 8.

% ===== SOFT CONSTRAINT 6: WEEKEND COVERAGE =====
% At least 2 different nurses must work weekend shifts
weekend_nurse(N) :- assigned(N, D, _), weekend(D).
weekend_count(C) :- C = #count{N : weekend_nurse(N)}.

% Violation: if fewer than 2 nurses work weekends, add 1 violation
violation_weekend(1) :- weekend_count(C), C < 2.
violation_weekend(0) :- weekend_count(C), C >= 2.

% ===== TOTAL VIOLATIONS =====
% Collect all violations into a single sum
violation_consecutive_total(V) :- V = #sum{V1, N : violation_consecutive(N, V1)}.
violation_fair_total(V) :- V = #sum{V2, N : violation_fair(N, V2)}.
violation_weekend_total(V) :- V = #sum{V3 : violation_weekend(V3)}.

total_violations(TV) :- 
    violation_consecutive_total(V1),
    violation_fair_total(V2),
    violation_weekend_total(V3),
    TV = V1 + V2 + V3.

% ===== OPTIMIZATION =====
#minimize{TV : total_violations(TV)}.

% ===== OUTPUT =====
#show assigned/3.
#show total_violations/1.