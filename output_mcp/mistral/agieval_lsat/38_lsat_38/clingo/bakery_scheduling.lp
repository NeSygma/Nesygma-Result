% Domains
cookie(oatmeal; peanut_butter; sugar).
batch(1; 2; 3).
day(monday; tuesday; wednesday; thursday; friday).

% Each batch is assigned to exactly one day
{ batch(C, B, D) : day(D) } = 1 :- cookie(C), batch(B).

% No two batches of the same kind on the same day
:- cookie(C), day(D), batch(B1; B2), B1 != B2, batch(C, B1, D), batch(C, B2, D).

% Exactly 3 batches of each kind (enforce this)
:- cookie(C), { batch(C, B, D) : day(D), batch(B) } != 3.

% At least one batch on Monday
:- not batch(_, _, monday).

% Second batch of oatmeal is made on the same day as first batch of peanut butter
:- batch(oatmeal, 2, D1), batch(peanut_butter, 1, D2), D1 != D2.
batch(oatmeal, 2, D) :- batch(peanut_butter, 1, D).
batch(peanut_butter, 1, D) :- batch(oatmeal, 2, D).

% Second batch of sugar cookies is made on Thursday
batch(sugar, 2, thursday).

% Count batches per day
batches_on_day(D, N) :- day(D), N = #count{ C, B : batch(C, B, D) }.

% Days with at most two batches
at_most_two(D) :- day(D), batches_on_day(D, N), N <= 2.

% Count how many days have at most two batches
num_days_at_most_two(N) :- N = #count{ D : at_most_two(D) }.

% Map the answer
option(a) :- num_days_at_most_two(1).
option(b) :- num_days_at_most_two(2).
option(c) :- num_days_at_most_two(3).
option(d) :- num_days_at_most_two(4).
option(e) :- num_days_at_most_two(5).

#show option/1.