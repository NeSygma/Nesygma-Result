% Define the domain
kind(oatmeal; peanut_butter; sugar).
day(monday; tuesday; wednesday; thursday; friday).
batch(1..3).

% Each batch of each kind is made on exactly one day
1 { made(K, B, D) : day(D) } 1 :- kind(K), batch(B).

% No two batches of the same kind are made on the same day
:- made(K, B1, D), made(K, B2, D), B1 != B2.

% At least one batch is made on Monday
:- not made(_, _, monday).

% The second batch of oatmeal cookies is made on the same day as the first batch of peanut butter cookies
made(oatmeal, 2, D) :- made(peanut_butter, 1, D).

% The second batch of sugar cookies is made on Thursday
made(sugar, 2, thursday).

% Condition: There exists a day where one kind's first batch and another kind's third batch coincide
condition_holds :- made(K1, 1, D), made(K2, 3, D), K1 != K2.
:- not condition_holds.

% Count the number of batches per day
batches_on_day(D, N) :- day(D), N = #count { K,B : made(K,B,D) }.

% Define the answer choices as they appear in the question:
% (A) At least one batch of cookies is made on each of the five days.
% This could be false if at least one day has no batches
answer(a) :- day(D), batches_on_day(D, 0).

% (B) At least two batches of cookies are made on Wednesday.
% This could be false if Wednesday has < 2 batches
answer(b) :- batches_on_day(wednesday, N), N < 2.

% (C) Exactly one batch of cookies is made on Monday.
% This could be false if Monday does not have exactly 1 batch
answer(c) :- batches_on_day(monday, N), N != 1.

% (D) Exactly two batches of cookies are made on Tuesday.
% This could be false if Tuesday does not have exactly 2 batches
answer(d) :- batches_on_day(tuesday, N), N != 2.

% (E) Exactly one batch of cookies is made on Friday.
% This could be false if Friday does not have exactly 1 batch
answer(e) :- batches_on_day(friday, N), N != 1.

% Ensure only one answer is selected
:- answer(X), answer(Y), X != Y.

#show answer/1.