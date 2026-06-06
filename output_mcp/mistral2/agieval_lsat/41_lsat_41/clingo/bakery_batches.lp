% --- Entities ---
cookie_type(oatmeal; peanut_butter; sugar).
day(monday; tuesday; wednesday; thursday; friday).
batch(T, 1..3) :- cookie_type(T).

% --- Choice Rule: Assign each batch to a day ---
{ made_on(T, B, D) : day(D) } = 1 :- cookie_type(T), batch(T, B).

% --- Constraints ---
% 1. No two batches of the same kind on the same day
:- made_on(T, B1, D), made_on(T, B2, D), B1 != B2.

% 2. At least one batch on Monday
:- day(D), not batches_on_day(D).
batches_on_day(D) :- made_on(_, _, D).

% 3. Second batch of oatmeal on the same day as first batch of peanut butter
:- made_on(oatmeal, 2, D), not made_on(peanut_butter, 1, D).

% 4. Second batch of sugar cookies on Thursday
:- not made_on(sugar, 2, thursday).

% 5. Exactly one batch on Friday
:- { made_on(_, _, friday) } != 1.

% --- Helper Predicates for Answer Choices ---
% A: The first batch of sugar cookies is made on Monday.
option(a) :- made_on(sugar, 1, monday).

% B: The first batch of oatmeal cookies is made on Tuesday.
option(b) :- made_on(oatmeal, 1, tuesday).

% C: The third batch of oatmeal cookies is made on Friday.
option(c) :- made_on(oatmeal, 3, friday).

% D: The first batch of peanut butter cookies is made on Wednesday.
option(d) :- made_on(peanut_butter, 1, wednesday).

% E: The second batch of peanut butter cookies is made on Tuesday.
option(e) :- made_on(peanut_butter, 2, tuesday).

% --- Show the answer ---
#show option/1.