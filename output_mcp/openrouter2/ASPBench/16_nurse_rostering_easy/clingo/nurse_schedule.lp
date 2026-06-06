% Domains
nurse(1). nurse(2). nurse(3). nurse(4).
day(1). day(2). day(3). day(4). day(5). day(6). day(7).
shift(1). shift(2). shift(3).

% Coverage requirements
required(1,2). required(2,1). required(3,1).

% Assignment: each shift gets exactly required number of nurses
:- day(D), shift(S), required(S,R), #count{N : assigned(N,D,S)} != R.

% Each nurse at most one shift per day
1 { assigned(N,D,S) : shift(S) } 1 :- nurse(N), day(D).

% Rest period: no night then morning next day
:- assigned(N,D,3), assigned(N,D1,1), D1 = D+1, day(D1).

% Total shifts per nurse
total_shifts(N, TS) :- TS = #count{D,S : assigned(N,D,S)}.

% Fairness violations
fair_violation(N, V) :- total_shifts(N, TS), TS < 6, V = 6 - TS.
fair_violation(N, V) :- total_shifts(N, TS), TS > 8, V = TS - 8.

% Consecutive days violations
violation_consecutive(N) :- assigned(N,D,_), assigned(N,D1,_), assigned(N,D2,_), assigned(N,D3,_), D1 = D-1, D2 = D-2, D3 = D-3, day(D), day(D1), day(D2), day(D3).

% Weekend nurses
weekend_nurse(N) :- assigned(N,D,_), day(D), D >= 6.

% Weekend coverage violation
violation_weekend :- #count{N : weekend_nurse(N)} < 2.

% Sum of violations
total_fair_violations(VF) :- VF = #sum{V : fair_violation(_, V)}.
total_consecutive_violations(VC) :- VC = #sum{1 : violation_consecutive(N)}.
total_weekend_violations(VW) :- VW = #count{1 : violation_weekend}.

violations(V) :- V = VF + VC + VW, total_fair_violations(VF), total_consecutive_violations(VC), total_weekend_violations(VW).

% Coverage met
coverage_met.

% Objective
#minimize { V@1 : violations(V) }.

% Show
#show assigned/3.
#show violations/1.
#show coverage_met.