% --- Facts ---
nurse(1..4).
day(1..7).
shift(1..3).  % 1: morning, 2: evening, 3: night

% Coverage requirements
required(1, 2).  % morning shift requires 2 nurses
required(2, 1).  % evening shift requires 1 nurse
required(3, 1).  % night shift requires 1 nurse

% Weekend days
weekend_day(6).
weekend_day(7).

% --- Choice Rule ---
% Assign nurses to shifts, ensuring at most one shift per nurse per day
{ assigned(Nurse, Day, Shift) : nurse(Nurse), shift(Shift) } <= 1 :- day(Day).

% --- Hard Constraints ---

% 1. Coverage requirement: Each shift must have exactly the required number of nurses
:- day(Day), shift(Shift), not required(Shift, Req),
   Req = #count { Nurse : assigned(Nurse, Day, Shift) }.

% 2. Single assignment: A nurse can work at most one shift per day (enforced by choice rule)

% 3. Rest period: A nurse cannot work night shift (3) on day D and morning shift (1) on day D+1
:- assigned(Nurse, Day, 3), assigned(Nurse, NextDay, 1),
   NextDay = Day + 1, day(NextDay).

% --- Soft Constraints ---

% 4. Max consecutive days: A nurse should not work more than 3 consecutive days
% Helper: Track consecutive assignments
consecutive(Nurse, Day, 1) :- assigned(Nurse, Day, _), day(Day).
consecutive(Nurse, Day, L+1) :- consecutive(Nurse, PrevDay, L), assigned(Nurse, Day, _),
                               Day = PrevDay + 1, day(Day), L < 3.
consecutive_violation(Nurse) :- nurse(Nurse),
                               #count { Day : consecutive(Nurse, Day, _) } > 3.

% 5. Fair distribution: Each nurse should work 6-8 shifts total
total_shifts(Nurse, Count) :- nurse(Nurse),
                              Count = #count { Day, Shift : assigned(Nurse, Day, Shift) }.
shift_violation(Nurse) :- total_shifts(Nurse, Count),
                          Count < 6.
shift_violation(Nurse) :- total_shifts(Nurse, Count),
                          Count > 8.

% 6. Weekend coverage: At least 2 different nurses must work weekend shifts
weekend_assignment(Nurse, Day) :- assigned(Nurse, Day, _), weekend_day(Day).
weekend_nurses(N) :- N = #count { Nurse : weekend_assignment(Nurse, _) }.
weekend_violation :- weekend_nurses(N), N < 2.

% --- Violation Counting ---
% Count violations
consecutive_violations(N) :- consecutive_violation(N).
shift_violations(N) :- shift_violation(N).
total_consecutive_violations(V) :- V = #sum { 1, N : consecutive_violations(N) }.
total_shift_violations(V) :- V = #sum { 1, N : shift_violations(N) }.
total_weekend_violations(1) :- weekend_violation.

% --- Objective ---
% Minimize total soft constraint violations
#minimize { V : total_consecutive_violations(V) }.
#minimize { V : total_shift_violations(V) }.
#minimize { V : total_weekend_violations(V) }.

% --- Show ---
#show assigned/3.
#show total_consecutive_violations/1.
#show total_shift_violations/1.
#show total_weekend_violations/1.