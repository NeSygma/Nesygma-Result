% Bakery cookie scheduling problem

% Days
day(mon). day(tue). day(wed). day(thu). day(fri).

% Kinds
kind(oat). kind(pb). kind(sugar).

% Batches: each kind has batches 1,2,3
batch(K, N) :- kind(K), N = 1..3.

% Assignment of each batch to a day
{ day(B, D) : day(D) } 1 :- batch(B, _).

% No batch on Wednesday
:- day(B, wed).

% At least one batch on Monday
:- not day(_, mon).

% No two batches of the same kind on the same day
:- day(B1, D), day(B2, D), B1 != B2, kind_of(B1, K), kind_of(B2, K).

% Helper: kind of a batch
kind_of(batch(K, _), K).

% Second batch of oatmeal and first batch of peanut butter on same day
day(batch(oat, 2), D) :- day(batch(pb, 1), D).

% Second batch of sugar on Thursday
day(batch(sugar, 2), thu).

% Count batches per day
batches_on_day(D, N) :- day(D), N = #count { B : day(B, D) }.

% Option conditions
option(a) :- batches_on_day(tue, 3).
option(b) :- batches_on_day(fri, 3).
option(c) :- batches_on_day(mon, N), N >= 2.
option(d) :- batches_on_day(thu, N), N >= 2.
option(e) :- batches_on_day(mon, M), batches_on_day(tue, T), M < T.

#show option/1.