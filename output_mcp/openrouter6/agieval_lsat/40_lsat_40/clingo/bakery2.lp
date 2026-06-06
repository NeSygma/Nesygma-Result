% Bakery cookie scheduling problem

% Days
day(mon). day(tue). day(wed). day(thu). day(fri).

% Kinds
kind(oat). kind(pb). kind(sugar).

% Batches: each kind has batches 1,2,3
batch(K, N) :- kind(K), N = 1..3.

% Assignment of each batch to a day
1 { day(K, N, D) : day(D) } 1 :- batch(K, N).

% No batch on Wednesday
:- day(_, _, wed).

% At least one batch on Monday
:- not day(_, _, mon).

% No two batches of the same kind on the same day
:- day(K, N1, D), day(K, N2, D), N1 != N2.

% Second batch of oatmeal and first batch of peanut butter on same day
day(oat, 2, D) :- day(pb, 1, D).

% Second batch of sugar on Thursday
day(sugar, 2, thu).

% Count batches per day
batches_on_day(D, Count) :- day(D), Count = #count { K, N : day(K, N, D) }.

% Option conditions
option(a) :- batches_on_day(tue, 3).
option(b) :- batches_on_day(fri, 3).
option(c) :- batches_on_day(mon, M), M >= 2.
option(d) :- batches_on_day(thu, N), N >= 2.
option(e) :- batches_on_day(mon, M), batches_on_day(tue, T), M < T.

#show option/1.