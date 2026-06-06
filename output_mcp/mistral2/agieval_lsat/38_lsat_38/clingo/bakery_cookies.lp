% Define the days of the week (Monday to Friday)
day(monday).
day(tuesday).
day(wednesday).
day(thursday).
day(friday).

% Define the types of cookies
cookie(oatmeal).
cookie(peanut_butter).
cookie(sugar).

% Define the batches (1, 2, 3 for each cookie type)
batch(1..3).

% A batch is assigned to a day and a cookie type
% We use a choice rule to allow the solver to assign batches to days and cookie types
{ assigned(Batch, Cookie, Day) : cookie(Cookie), day(Day) } 1 :- batch(Batch).

% Ensure that no two batches of the same kind of cookie are made on the same day
:- assigned(B1, Cookie, Day), assigned(B2, Cookie, Day), B1 != B2.

% Ensure that exactly three batches of each kind of cookie are made each week
:- cookie(Cookie), { assigned(Batch, Cookie, _) : batch(Batch) } != 3.

% Ensure that at least one batch of cookies is made on Monday
at_least_one_monday :- assigned(_, _, monday).
:- not at_least_one_monday.

% The second batch of oatmeal cookies is made on the same day as the first batch of peanut butter cookies
% This is enforced by ensuring that if batch 2 of oatmeal is assigned to a day, batch 1 of peanut_butter must also be assigned to the same day
:- assigned(2, oatmeal, Day1), assigned(1, peanut_butter, Day2), Day1 != Day2.

% The second batch of sugar cookies is made on Thursday
:- not assigned(2, sugar, thursday).

% Count the number of days with at most two batches of cookies
% A day has at most two batches if the number of batches assigned to it is <= 2
day_has_at_most_two_batches(Day) :- day(Day), { assigned(_, _, Day) } <= 2.

% Count the number of days with at most two batches
num_days_at_most_two(Count) :- Count = #count{ Day : day_has_at_most_two_batches(Day) }.

% Map the correct answer to option/1 (MANDATORY)
option(a) :- num_days_at_most_two(1).
option(b) :- num_days_at_most_two(2).
option(c) :- num_days_at_most_two(3).
option(d) :- num_days_at_most_two(4).
option(e) :- num_days_at_most_two(5).

#show option/1.