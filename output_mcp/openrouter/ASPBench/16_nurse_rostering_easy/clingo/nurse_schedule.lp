% Domains
nurse(1..4).
day(1..7).
shift(1..3).

% Coverage requirements per shift (shift id, required count)
required(1,2). % morning
required(2,1). % evening
required(3,1). % night

% Choice: assign exactly required number of nurses to each shift
{ work(N,D,S) : nurse(N) } = R :- day(D), shift(S), required(S,R).

% Hard constraints
% 1. At most one shift per nurse per day
:- work(N,D,S1), work(N,D,S2), S1 != S2.

% 2. Rest: no night (3) then morning (1) next day
:- work(N,D,3), D < 7, work(N,D+1,1).

% Derived predicate: nurse works on a day (any shift)
works(N,D) :- work(N,D,_).

% Soft constraint 4: consecutive days >3
violation_consec(N) :- nurse(N), day(D), D >= 4,
    works(N,D), works(N,D-1), works(N,D-2), works(N,D-3).

% Soft constraint 5: fair distribution (6-8 shifts)
total_shifts(N,T) :- nurse(N), T = #count{ D,S : work(N,D,S) }.
violation_fair_low(N) :- total_shifts(N,T), T < 6.
violation_fair_high(N) :- total_shifts(N,T), T > 8.

% Soft constraint 6: weekend coverage (days 6 and 7)
weekend_nurse(N) :- work(N,6,_).
weekend_nurse(N) :- work(N,7,_).
violation_weekend :- #count{ N : weekend_nurse(N) } < 2.

% Collect all violation atoms
violation(consec(N)) :- violation_consec(N).
violation(fair_low(N)) :- violation_fair_low(N).
violation(fair_high(N)) :- violation_fair_high(N).
violation(weekend) :- violation_weekend.

% Total violations
total_violations(V) :- V = #sum{ 1, Vtype : violation(Vtype) }.

% Optimization: minimize total violations
#minimize { 1, Vtype : violation(Vtype) }.

#show work/3.
#show total_violations/1.