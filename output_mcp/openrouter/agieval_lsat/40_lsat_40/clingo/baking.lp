% Days (Wednesday excluded)
day(mon). day(tue). day(thu). day(fri).

% Kinds
kind(oat). kind(pb). kind(sug).

% Batches
batch(1). batch(2). batch(3).

% Assign each batch of each kind to exactly one day
1 { d(K,B,D) : day(D) } 1 :- kind(K), batch(B).

% No two batches of same kind on same day
:- d(K,B1,D), d(K,B2,D), B1 != B2.

% At least one batch on Monday
:- not monday_batch.
monday_batch :- d(_,_,mon).

% Oatmeal batch 2 same day as Peanut batch 1
:- d(oat,2,D1), d(pb,1,D2), D1 != D2.

% Sugar batch 2 is on Thursday
:- d(sug,2,D), D != thu.

% Count batches per day
cnt(D,N) :- day(D), N = #count { K,B : d(K,B,D) }.

% Options
option(a) :- cnt(tue,3).
option(b) :- cnt(fri,3).
option(c) :- cnt(mon,N), N >= 2.
option(d) :- cnt(thu,N), N >= 2.
option(e) :- cnt(mon,M), cnt(tue,T), M < T.

#show option/1.