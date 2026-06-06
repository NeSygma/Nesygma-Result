% Define the days of the week (Monday to Friday)
day(monday; tuesday; wednesday; thursday; friday).

% Define the types of cookies
cookie(oatmeal; peanut_butter; sugar).

% Define the batches (1, 2, 3 for each cookie type)
batch(1..3).

% Assign batches to days (choice rule)
{ batch(Cookie, BatchNum, Day) : day(Day) } = 1 :-
    cookie(Cookie),
    batch(BatchNum).

% Ensure no two batches of the same kind are made on the same day
:- cookie(Cookie),
   day(Day),
   batch(BatchNum1),
   batch(BatchNum2),
   BatchNum1 != BatchNum2,
   batch(Cookie, BatchNum1, Day),
   batch(Cookie, BatchNum2, Day).

% Ensure exactly three batches of each cookie type are made
:- cookie(Cookie),
   Count = #count { BatchNum, Day : batch(Cookie, BatchNum, Day) },
   Count != 3.

% At least one batch of cookies is made on Monday
:- not batch(_, _, monday).

% The second batch of oatmeal cookies is made on the same day as the first batch of peanut butter cookies
:- batch(oatmeal, 2, Day),
   not batch(peanut_butter, 1, Day).

% The second batch of sugar cookies is made on Thursday
:- not batch(sugar, 2, thursday).

% No batch of cookies is made on Wednesday
:- batch(_, _, wednesday).

% Count the number of batches per day
batches_on_day(Day, Count) :-
    day(Day),
    Count = #count { Cookie, BatchNum : batch(Cookie, BatchNum, Day) }.

% Define the conditions for each option
% Option A: Exactly three batches of cookies are made on Tuesday
option(a) :- batches_on_day(tuesday, 3).

% Option B: Exactly three batches of cookies are made on Friday
option(b) :- batches_on_day(friday, 3).

% Option C: At least two batches of cookies are made on Monday
option(c) :- batches_on_day(monday, Count), Count >= 2.

% Option D: At least two batches of cookies are made on Thursday
option(d) :- batches_on_day(thursday, Count), Count >= 2.

% Option E: Fewer batches of cookies are made on Monday than on Tuesday
option(e) :- batches_on_day(monday, M), batches_on_day(tuesday, T), M < T.

% Ensure only one option is true
:- option(X), option(Y), X != Y.

% Final answer mapping
answer(a) :- option(a).
answer(b) :- option(b).
answer(c) :- option(c).
answer(d) :- option(d).
answer(e) :- option(e).

#show answer/1.