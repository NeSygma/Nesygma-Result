% Define domains
cookie(oatmeal; peanut_butter; sugar).
day(monday; tuesday; wednesday; thursday; friday).
batch(1..3).

% Assign batches to days
% Each batch of each cookie type must be assigned to exactly one day
{ assigned(Cookie, Batch, Day) : day(Day) } = 1 :- cookie(Cookie), batch(Batch).

% Exactly 3 batches per cookie type (redundant with the choice rule but explicit)
:- cookie(Cookie), #count{Day, Batch : assigned(Cookie, Batch, Day)} != 3.

% No two batches of same kind on same day
:- cookie(Cookie), day(Day), batch(B1), batch(B2), B1 != B2, assigned(Cookie, B1, Day), assigned(Cookie, B2, Day).

% At least one batch on Monday
:- not assigned(_, _, monday).

% Second batch of oatmeal is on same day as first batch of peanut butter
:- assigned(oatmeal, 2, Day), not assigned(peanut_butter, 1, Day).
:- assigned(peanut_butter, 1, Day), not assigned(oatmeal, 2, Day).

% Second batch of sugar is on Thursday
:- not assigned(sugar, 2, thursday).

% Friday has exactly one batch
:- #count{Cookie, Batch : assigned(Cookie, Batch, friday)} != 1.

% Define the options as mutually exclusive possibilities
% Option A: First batch of sugar cookies is made on Monday
option(a) :- assigned(sugar, 1, monday).

% Option B: First batch of oatmeal cookies is made on Tuesday
option(b) :- assigned(oatmeal, 1, tuesday).

% Option C: Third batch of oatmeal cookies is made on Friday
option(c) :- assigned(oatmeal, 3, friday).

% Option D: First batch of peanut butter cookies is made on Wednesday
option(d) :- assigned(peanut_butter, 1, wednesday).

% Option E: Second batch of peanut butter cookies is made on Tuesday
option(e) :- assigned(peanut_butter, 2, tuesday).

% Ensure only one option is true at a time
:- option(X), option(Y), X != Y.

#show option/1.