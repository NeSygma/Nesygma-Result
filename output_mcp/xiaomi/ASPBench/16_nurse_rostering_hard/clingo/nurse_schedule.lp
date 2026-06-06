% Domain definitions
nurse(1..5).
day(1..10).
shift(1..3).

% Choice rule: assign nurses to shifts (at most one per day)
{ assigned(N, D, S) : shift(S) } 1 :- nurse(N), day(D).

% Coverage constraints: exactly required number per shift per day
% Morning shift (1): exactly 2 nurses
:- day(D), #count{ N : assigned(N, D, 1) } != 2.

% Evening shift (2): exactly 1 nurse
:- day(D), #count{ N : assigned(N, D, 2) } != 1.

% Night shift (3): exactly 1 nurse
:- day(D), #count{ N : assigned(N, D, 3) } != 1.

% Helper predicates for rest constraint
works_night(N, D) :- assigned(N, D, 3).
works_morning(N, D) :- assigned(N, D, 1).

% Rest constraint: night shift on day D → no morning shift on day D+1
:- works_night(N, D), works_morning(N, D+1), day(D), day(D+1).

% Output: show assignments
#show assigned/3.