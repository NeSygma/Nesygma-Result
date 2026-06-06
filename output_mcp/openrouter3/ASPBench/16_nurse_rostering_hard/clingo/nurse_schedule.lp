% Nurse Scheduling Problem
% 5 nurses, 10 days, 3 shifts per day

% Domain declarations
nurse(1..5).
day(1..10).
shift(1..3).

% Choice rule: Each nurse can be assigned to at most one shift per day
% We use a choice rule to allow any assignment, then constrain it
{ assigned(N, D, S) : shift(S) } 1 :- nurse(N), day(D).

% Constraint 1: Coverage requirements
% Morning shift (1) must have exactly 2 nurses
:- day(D), shift(1), #count{ N : assigned(N, D, 1) } != 2.

% Evening shift (2) must have exactly 1 nurse
:- day(D), shift(2), #count{ N : assigned(N, D, 2) } != 1.

% Night shift (3) must have exactly 1 nurse
:- day(D), shift(3), #count{ N : assigned(N, D, 3) } != 1.

% Constraint 2: Single assignment per day (already enforced by choice rule with cardinality 1)

% Constraint 3: Rest period
% If a nurse works night shift (3) on day D, they cannot work morning shift (1) on day D+1
:- assigned(N, D, 3), assigned(N, D+1, 1), day(D), day(D+1).

% Show the roster in a readable format
% For each day, show which nurses are assigned to which shifts
#show assigned/3.

% Alternative: Show roster as a structured output
roster(D, 1, N) :- assigned(N, D, 1).
roster(D, 2, N) :- assigned(N, D, 2).
roster(D, 3, N) :- assigned(N, D, 3).
#show roster/3.