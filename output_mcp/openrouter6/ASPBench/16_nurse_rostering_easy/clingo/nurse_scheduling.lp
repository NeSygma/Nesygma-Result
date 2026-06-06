% Nurse Scheduling Problem
% 4 nurses, 7 days, 3 shifts per day

% ==================== DOMAINS ====================
nurse(1..4).
day(1..7).
shift(1..3). % 1=morning, 2=evening, 3=night

% Coverage requirements per shift
required(1, 2). % morning: 2 nurses
required(2, 1). % evening: 1 nurse  
required(3, 1). % night: 1 nurse

% ==================== DECISION VARIABLES ====================
% works(N, D, S): nurse N works shift S on day D
% Each nurse can work at most one shift per day
{ works(N, D, S) : shift(S) } 1 :- nurse(N), day(D).

% ==================== HARD CONSTRAINTS ====================
% 1. Coverage requirement: exactly required number of nurses per shift
:- day(D), shift(S), required(S, Req),
   N = #count{ N : works(N, D, S) },
   N != Req.

% 2. Single assignment: already enforced by choice rule (at most 1)

% 3. Rest period: cannot work night shift then morning shift next day
:- works(N, D, 3), works(N, D+1, 1), day(D), day(D+1).

% ==================== HELPER PREDICATES ====================
% worked(N, D): nurse N works any shift on day D
worked(N, D) :- works(N, D, _).

% weekend_day(D): days 6-7 are weekend
weekend_day(6). weekend_day(7).

% ==================== SOFT CONSTRAINTS ====================
% 4. Max consecutive days: not more than 3 consecutive days
% Count consecutive work days for each nurse

% Check if a nurse works 4 consecutive days starting at D
violation_consecutive(N, D) :-
    worked(N, D), worked(N, D+1), worked(N, D+2), worked(N, D+3),
    day(D), day(D+1), day(D+2), day(D+3).

% 5. Fair distribution: each nurse should work 6-8 shifts total
total_shifts(N, Total) :-
    nurse(N),
    Total = #count{ D, S : works(N, D, S) }.

violation_fair(N) :-
    nurse(N),
    total_shifts(N, Total),
    (Total < 6 ; Total > 8).

% 6. Weekend coverage: at least 2 different nurses must work weekend shifts
% Count nurses who work at least one weekend shift
weekend_nurse(N) :-
    nurse(N),
    worked(N, D), weekend_day(D).

weekend_nurse_count(Count) :-
    Count = #count{ N : weekend_nurse(N) }.

violation_weekend :-
    weekend_nurse_count(Count),
    Count < 2.

% ==================== VIOLATION COUNTING ====================
% Count violations for each soft constraint
violation_count_consecutive(Count) :-
    Count = #count{ N, D : violation_consecutive(N, D) }.

violation_count_fair(Count) :-
    Count = #count{ N : violation_fair(N) }.

violation_count_weekend(1) :- violation_weekend.
violation_count_weekend(0) :- not violation_weekend.

% Total violations - sum all individual violations
total_violations(Total) :-
    violation_count_consecutive(C1),
    violation_count_fair(C2),
    violation_count_weekend(C3),
    Total = C1 + C2 + C3.

% ==================== OBJECTIVE ====================
#minimize { V : total_violations(V) }.

% ==================== OUTPUT ====================
% Coverage met (must be true for valid solution)
coverage_met :- not violation_coverage.
violation_coverage :- day(D), shift(S), required(S, Req),
                      N = #count{ N : works(N, D, S) }, N != Req.

% Show roster in structured format
% For each day, show morning, evening, night assignments
roster_day(D, "morning", N1, N2) :-
    day(D),
    works(N1, D, 1), works(N2, D, 1), N1 < N2,
    required(1, 2).

roster_day(D, "evening", N) :-
    day(D),
    works(N, D, 2),
    required(2, 1).

roster_day(D, "night", N) :-
    day(D),
    works(N, D, 3),
    required(3, 1).

% Show violations breakdown
show_violations :-
    violation_count_consecutive(C1),
    violation_count_fair(C2),
    violation_count_weekend(C3),
    total_violations(Total).

% Show total violations
#show violations/1.
#show coverage_met/0.
#show roster_day/4.
#show show_violations/0.

% For cleaner output, show only the essential information
#show works/3.
#show total_violations/1.