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
:- not assigned(_, _, monday).

% Condition: second oatmeal batch same day as first peanut butter batch
:- assigned(oatmeal, 2, Day1), assigned(peanut_butter, 1, Day2), Day1 != Day2.

% Condition: second sugar batch on Thursday
assigned(sugar, 2, thursday).

% Exactly one batch on Friday
:- 2 { assigned(_, _, friday) }.
:- not assigned(_, _, friday).

% Check which options are possible
opt_a :- assigned(sugar, 1, monday).
opt_b :- assigned(oatmeal, 1, tuesday).
opt_c :- assigned(oatmeal, 3, friday).
opt_d :- assigned(peanut_butter, 1, wednesday).
opt_e :- assigned(peanut_butter, 2, tuesday).

#show assigned/3.
#show opt_a/0.
#show opt_b/0.
#show opt_c/0.
#show opt_d/0.
#show opt_e/0.