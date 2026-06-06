% --- Domains ---
nurse(1..4).
day(1..7).
shift(1..3).
shift_req(1, 2).
shift_req(2, 1).
shift_req(3, 1).

% --- Decision Variables ---
{ assign(N, D, S) : shift(S) } 1 :- nurse(N), day(D).

% --- Hard Constraints ---
% 1. Coverage requirement
:- day(D), shift(S), shift_req(S, R),
   #count { N : assign(N, D, S) } != R.

% 2. Rest period: No night shift (3) then morning shift (1) next day
:- nurse(N), day(D), D < 7,
   assign(N, D, 3), assign(N, D+1, 1).

% --- Soft Constraints ---
works(N, D) :- assign(N, D, _).

% 4. Max consecutive days: Not more than 3 consecutive days
% Each day beyond 3 consecutive adds 1 violation
violation_consecutive(N, D) :- nurse(N), day(D), D >= 4,
                               works(N, D), works(N, D-1), works(N, D-2), works(N, D-3).

% 5. Fair distribution: 6-8 shifts total
total_shifts(N, T) :- nurse(N), T = #count { D : works(N, D) }.
violation_dist(N, V) :- nurse(N), total_shifts(N, T), T < 6, V = 6 - T.
violation_dist(N, V) :- nurse(N), total_shifts(N, T), T > 8, V = T - 8.

% 6. Weekend coverage: At least 2 different nurses must work weekend shifts (days 6-7)
weekend_worker(N) :- nurse(N), assign(N, 6, _).
weekend_worker(N) :- nurse(N), assign(N, 7, _).
count_weekend(C) :- C = #count { N : weekend_worker(N) }.
violation_weekend :- count_weekend(C), C < 2.

% --- Objective ---
#minimize { 1, N, D : violation_consecutive(N, D) ; 
            V, N : violation_dist(N, V) ; 
            1 : violation_weekend }.

% --- Output ---
#show assign/3.
#show violation_consecutive/2.
#show violation_dist/2.
#show violation_weekend/0.