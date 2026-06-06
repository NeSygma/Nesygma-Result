% Nurse Scheduling Problem

% Domains
nurse(1..5).
day(1..10).
shift(1..3).

% Assignment: nurse works a shift on a day
% At most one shift per nurse per day
0 { assigned(Nurse, Day, Shift) : shift(Shift) } 1 :- nurse(Nurse), day(Day).

% Coverage requirements per shift per day
% Morning shift (1): exactly 2 nurses
2 { assigned(Nurse, Day, 1) : nurse(Nurse) } 2 :- day(Day).
% Evening shift (2): exactly 1 nurse
1 { assigned(Nurse, Day, 2) : nurse(Nurse) } 1 :- day(Day).
% Night shift (3): exactly 1 nurse
1 { assigned(Nurse, Day, 3) : nurse(Nurse) } 1 :- day(Day).

% Rest period: if a nurse works night shift on day D, cannot work morning shift on day D+1
:- assigned(Nurse, Day, 3), assigned(Nurse, Day+1, 1), day(Day), day(Day+1).

% Show assignments
#show assigned/3.