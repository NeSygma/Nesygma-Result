% Domains
cookie(oatmeal; peanut_butter; sugar).
batch(1; 2; 3).
day(mon; tue; wed; thu; fri).

% Each batch is made on a single day
1 { made(C, B, D) : day(D) } 1 :- cookie(C), batch(B).

% No two batches of the same kind are made on the same day
:- made(C, B1, D), made(C, B2, D), B1 != B2.

% At least one batch of cookies is made on Monday
:- not 1 { made(C, B, mon) : cookie(C), batch(B) }.

% The second batch of oatmeal cookies is made on the same day as the first batch of peanut butter cookies
made(oatmeal, 2, D) :- made(peanut_butter, 1, D).
made(peanut_butter, 1, D) :- made(oatmeal, 2, D).

% The second batch of sugar cookies is made on Thursday
made(sugar, 2, thu).

% Condition: one kind's first batch is made on the same day as another kind's third batch
condition :- cookie(C1), cookie(C2), C1 != C2, made(C1, 1, D), made(C2, 3, D).
:- not condition.

% Options
day_has_batch(D) :- day(D), 1 { made(C, B, D) : cookie(C), batch(B) }.
all_days_covered_all :- #count{D : day_has_batch(D)} = 5.

at_least_two_wed :- 2 { made(C, B, wed) : cookie(C), batch(B) }.
exactly_one_mon :- #count{C, B : made(C, B, mon)} = 1.
exactly_two_tue :- #count{C, B : made(C, B, tue)} = 2.
exactly_one_fri :- #count{C, B : made(C, B, fri)} = 1.

% An option is necessarily true if it is true in ALL models.
% An option could be false if there exists at least one model where it is false.

% We want to find which of these is NOT necessarily true.
% Let's define "necessarily_true(X)"
necessarily_true(a) :- all_days_covered_all.
necessarily_true(b) :- at_least_two_wed.
necessarily_true(c) :- exactly_one_mon.
necessarily_true(d) :- exactly_two_tue.
necessarily_true(e) :- exactly_one_fri.

% We want to find the option that is NOT necessarily true.
% Wait, the question asks "which one of the following could be false?".
% This is equivalent to "which one of the following is NOT necessarily true?".

% Let's check which options are NOT necessarily true.
not_necessarily_true(X) :- not necessarily_true(X), X = a.
not_necessarily_true(X) :- not necessarily_true(X), X = b.
not_necessarily_true(X) :- not necessarily_true(X), X = c.
not_necessarily_true(X) :- not necessarily_true(X), X = d.
not_necessarily_true(X) :- not necessarily_true(X), X = e.

#show not_necessarily_true/1.