% Days of the week
day(mon). day(tue). day(wed). day(thu). day(fri).

% Cookie types
cookie(oatmeal). cookie(peanut_butter). cookie(sugar).

% Batch numbers (1, 2, 3 for each type)
batch(1). batch(2). batch(3).

% Assign each batch of each cookie type to a day
{ assign(Cookie, Batch, Day) : day(Day) } 1 :- cookie(Cookie), batch(Batch).

% Constraint 1: No two batches of same cookie type on same day
:- assign(Cookie, B1, Day), assign(Cookie, B2, Day), B1 != B2.

% Constraint 2: At least one batch on Monday
:- not assign(_, _, mon).

% Constraint 3: Second oatmeal batch = first peanut butter batch (same day)
assign(peanut_butter, 1, Day) :- assign(oatmeal, 2, Day).
assign(oatmeal, 2, Day) :- assign(peanut_butter, 1, Day).

% Constraint 4: Second sugar batch = Thursday
assign(sugar, 2, thu).

% Count batches per day
batches_on_day(Day, N) :- day(Day), N = #count{ Cookie, Batch : assign(Cookie, Batch, Day) }.

% A day has "at most 2 batches" if batches_on_day(Day, N) and N <= 2
at_most_two(Day) :- day(Day), batches_on_day(Day, N), N <= 2.

% Count how many days have at most 2 batches
count_at_most_two(N) :- N = #count{ Day : at_most_two(Day) }.

% Map to answer choices
option(a) :- count_at_most_two(1).
option(b) :- count_at_most_two(2).
option(c) :- count_at_most_two(3).
option(d) :- count_at_most_two(4).
option(e) :- count_at_most_two(5).

#show option/1.
#show assign/3.
#show batches_on_day/2.
#show at_most_two/1.