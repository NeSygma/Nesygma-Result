% Domains
nurse(1..5).
day(1..10).
shift(1). shift(2). shift(3).

% Helper for next day
next_day(D, D+1) :- day(D), D < 10.

% Choice: assign nurse N to shift S on day D (or not)
{ assigned(N, D, S) } :- nurse(N), day(D), shift(S).

% Constraint 1: Coverage requirements
% Morning shift (1) exactly 2 nurses per day
:- day(D), #count{ N : assigned(N, D, 1) } != 2.
% Evening shift (2) exactly 1 nurse per day
:- day(D), #count{ N : assigned(N, D, 2) } != 1.
% Night shift (3) exactly 1 nurse per day
:- day(D), #count{ N : assigned(N, D, 3) } != 1.

% Constraint 2: Single assignment per day
:- assigned(N, D, S1), assigned(N, D, S2), S1 != S2.

% Constraint 3: Rest period - no morning shift after night shift
:- assigned(N, D, 3), assigned(N, D2, 1), next_day(D, D2).

% Show assignments
#show assigned/3.