% Facts
witness(franco). witness(garcia). witness(hong). witness(iturbe). witness(jackson).

day_of_week(monday). day_of_week(tuesday). day_of_week(wednesday).

% Each witness assigned to exactly one day
1 { day(W, D) : day_of_week(D) } 1 :- witness(W).

% Constraints
:- day(franco, D), day(garcia, D). % Franco not same day as Garcia

day(iturbe, wednesday). % Iturbe Wednesday
:- day(iturbe, D), D != wednesday. % Iturbe only Wednesday
:- day(hong, monday). % Hong not Monday

% Franco same day as Hong
day(franco, D) :- day(hong, D).
day(hong, D) :- day(franco, D).

% Exactly two on Tuesday
:- #count{W : day(W, tuesday)} != 2.
% At least one on Monday
:- #count{W : day(W, monday)} < 1.

% Option rules
option(a) :- day(franco, wednesday).
option(b) :- day(garcia, monday).
option(c) :- day(garcia, wednesday).
option(d) :- day(hong, tuesday).
option(e) :- day(iturbe, wednesday), not day(franco, wednesday), not day(garcia, wednesday), not day(hong, wednesday), not day(jackson, wednesday).

#show option/1.