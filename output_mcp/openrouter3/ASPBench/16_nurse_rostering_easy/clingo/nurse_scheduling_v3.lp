% Nurse Scheduling Problem - Version 3

% Domain declarations
nurse(1..4).
day(1..7).
shift(morning; evening; night).

% Coverage requirements
coverage_req(morning, 2).
coverage_req(evening, 1).
coverage_req(night, 1).

% Decision variables: which nurse works which shift on which day
{ works(N, D, S) : nurse(N) } 1 :- day(D), shift(S).

% HARD CONSTRAINT 1: Coverage requirements
% Count nurses working each shift each day
coverage(D, S, Count) :- day(D), shift(S), Count = #count{ N : works(N, D, S) }.
:- coverage(D, S, Count), coverage_req(S, Req), Count != Req.

% HARD CONSTRAINT 2: Single assignment per day per nurse
% At most one shift per day per nurse
:- works(N, D, S1), works(N, D, S2), S1 != S2.

% HARD CONSTRAINT 3: Rest period - no night shift followed by morning next day
% Night shift ends at 8am, morning starts at 6am next day (only 10 hours rest)
:- works(N, D, night), works(N, D+1, morning).

% SOFT CONSTRAINT 4: Max consecutive days (3 consecutive max)
% Count consecutive days worked
consecutive_days(N, D, 1) :- works(N, D, _), not works(N, D-1, _).
consecutive_days(N, D, C+1) :- works(N, D, _), works(N, D-1, _), consecutive_days(N, D-1, C).

% Violation for working more than 3 consecutive days
% Each day beyond 3 consecutive adds 1 violation
consecutive_violation(N, D) :- consecutive_days(N, D, C), C > 3.

% SOFT CONSTRAINT 5: Fair distribution (6-8 shifts per nurse)
total_shifts(N, Count) :- nurse(N), Count = #count{ D, S : works(N, D, S) }.

% Violations for shifts outside 6-8 range
below_min(N) :- total_shifts(N, Count), Count < 6.
above_max(N) :- total_shifts(N, Count), Count > 8.

% SOFT CONSTRAINT 6: Weekend coverage (days 6-7)
% At least 2 different nurses must work weekend shifts
weekend_nurse(N) :- works(N, 6, _); works(N, 7, _).
weekend_nurse_count(Count) :- Count = #count{ N : weekend_nurse(N) }.
weekend_violation :- weekend_nurse_count(Count), Count < 2.

% Calculate total violations
consecutive_violation_count(CV) :- CV = #count{ N, D : consecutive_violation(N, D) }.
below_min_count(BM) :- BM = #count{ N : below_min(N) }.
above_max_count(AM) :- AM = #count{ N : above_max(N) }.
weekend_violation_count(WV) :- WV = #count{ : weekend_violation }.

violation_count(V) :-
    consecutive_violation_count(CV),
    below_min_count(BM),
    above_max_count(AM),
    weekend_violation_count(WV),
    V = CV + BM + AM + WV.

% Objective: minimize total violations
#minimize { V : violation_count(V) }.

% Show solution
#show works/3.
#show violation_count/1.
#show coverage/3.