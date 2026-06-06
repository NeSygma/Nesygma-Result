% Days of the week
day(monday).
day(tuesday).
day(wednesday).
day(thursday).
day(friday).

% Cookie types
type(oatmeal).
type(peanut_butter).
type(sugar).

% Batch numbers
batch(1).
batch(2).
batch(3).

% Each batch is assigned to exactly one day
1 { assigned(Type, Batch, Day) : day(Day) } 1 :- type(Type), batch(Batch).

% No two batches of the same type on the same day
:- assigned(Type, B1, Day), assigned(Type, B2, Day), B1 != B2.

% At least one batch on Monday
made_on_monday :- assigned(_, _, monday).
:- not made_on_monday.

% Condition 3: second oatmeal batch same day as first peanut butter batch
:- assigned(oatmeal, 2, Day1), assigned(peanut_butter, 1, Day2), Day1 != Day2.

% Condition 4: second sugar batch on Thursday
assigned(sugar, 2, thursday).

% Exactly one batch on Friday
friday_count(N) :- N = #count{ Type, Batch : assigned(Type, Batch, friday) }.
:- friday_count(N), N != 1.

% Choice over answer options
{ option(a); option(b); option(c); option(d); option(e) } 1.

% Impose condition for each option if chosen
:- option(a), not assigned(sugar, 1, monday).
:- option(b), not assigned(oatmeal, 1, tuesday).
:- option(c), not assigned(oatmeal, 3, friday).
:- option(d), not assigned(peanut_butter, 1, wednesday).
:- option(e), not assigned(peanut_butter, 2, tuesday).

#show option/1.