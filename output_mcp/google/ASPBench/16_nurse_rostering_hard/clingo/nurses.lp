% --- Domains ---
nurse(1..5).
day(1..10).
shift(1..3).

% --- Generation ---
% Each nurse can be assigned to a shift on a day.
{ assigned(N, S, D) } :- nurse(N), shift(S), day(D).

% --- Constraints ---

% 1. Coverage Requirements
% Morning Shift (1): Exactly 2 nurses
:- day(D), #count { N : assigned(N, 1, D) } != 2.

% Evening Shift (2): Exactly 1 nurse
:- day(D), #count { N : assigned(N, 2, D) } != 1.

% Night Shift (3): Exactly 1 nurse
:- day(D), #count { N : assigned(N, 3, D) } != 1.

% 2. Single Assignment per Day
% A nurse can be assigned to at most one shift on any given day.
:- nurse(N), day(D), #count { S : assigned(N, S, D) } > 1.

% 3. Rest Period
% A nurse who works a night shift (3) on any day cannot work the morning shift (1) on the following day.
:- assigned(N, 3, D), assigned(N, 1, D+1), day(D), day(D+1).

% --- Output ---
#show assigned/3.