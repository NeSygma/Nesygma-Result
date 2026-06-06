%% Domain definitions
nurse(1..4).
day(1..7).
shift(1..3).

% Shift types and their requirements
shift_type(1, morning).
shift_type(2, evening).
shift_type(3, night).

% Coverage requirements per shift type
coverage_required(1, 2).  % Morning: 2 nurses
coverage_required(2, 1).  % Evening: 1 nurse
coverage_required(3, 1).  % Night: 1 nurse

% Weekend days
weekend(6).
weekend(7).

% Weekend shift types (morning and evening are considered weekend shifts)
weekend_shift(S) :- shift_type(S, morning).
weekend_shift(S) :- shift_type(S, evening).

%% Choice rule for assignments
% A nurse can be assigned to at most one shift per day
{ assigned(N, D, S) : nurse(N), shift(S) } 1 :- day(D).

%% Hard Constraint 1: Coverage requirement
% Each shift must have exactly the required number of nurses
:- shift_type(S, _), day(D),
   not #count { N : assigned(N, D, S) } = Req,
   coverage_required(S, Req).

%% Hard Constraint 2: Single assignment (enforced by choice rule)
% Already enforced by the choice rule above

%% Hard Constraint 3: Rest period
% A nurse cannot work night shift (ends 8am) then morning shift next day (starts 6am)
% Night shift ends at 8am, morning shift starts at 6am the next day
% This means if a nurse works night shift on day D, they cannot work morning shift on day D+1
:- assigned(N, D, 3), assigned(N, D+1, 1), day(D), day(D+1).

%% Soft Constraint 4: Max consecutive days (more than 3 consecutive days)
% Compute consecutive days worked for each nurse
consecutive_days(N, D, 1) :- assigned(N, D, _), day(D), not assigned(N, D-1, _).
consecutive_days(N, D, C+1) :- consecutive_days(N, D-1, C), assigned(N, D, _), day(D), day(D-1), C < 4.

% Violation: working 4 or more consecutive days
violation_consec(N, D) :- consecutive_days(N, D, C), C >= 4, nurse(N), day(D).

%% Soft Constraint 5: Fair distribution (6-8 shifts total)
total_shifts(N, C) :- C = #count { D, S : assigned(N, D, S) }, nurse(N).

% Violation: shifts < 6 or > 8
violation_shifts(N) :- total_shifts(N, C), C < 6, nurse(N).
violation_shifts(N) :- total_shifts(N, C), C > 8, nurse(N).

%% Soft Constraint 6: Weekend coverage (at least 2 different nurses)
weekend_nurse(N) :- assigned(N, D, S), weekend(D), nurse(N), weekend_shift(S).

% Violation: fewer than 2 nurses work weekend shifts
:- { weekend_nurse(N) } < 2.

% Helper predicate for weekend violation
violation_weekend :- { weekend_nurse(N) } < 2.

%% Compute total violations
% Count consecutive violations
consecutive_violation_count(C) :- C = #count { N, D : violation_consec(N, D) }.

% Count shifts violations
shifts_violation_count(S) :- S = #count { N : violation_shifts(N) }.

% Count weekend violations
weekend_violation_count(1) :- violation_weekend.
weekend_violation_count(0) :- not violation_weekend.

% Total violations
1 { total_violations(T) : T = C + S + W } 1 :-
    consecutive_violation_count(C),
    shifts_violation_count(S),
    weekend_violation_count(W).

% Show the assignments and violations
#show assigned/3.
#show total_shifts/2.
#show violation_consec/2.
#show violation_shifts/1.
#show violation_weekend/0.

#show total_violations/1.

% Check if coverage is met (all hard constraints satisfied)
coverage_met :- not coverage_violation.
coverage_violation :- shift_type(S, _), day(D),
                     not #count { N : assigned(N, D, S) } = Req,
                     coverage_required(S, Req).

#show coverage_met/0.