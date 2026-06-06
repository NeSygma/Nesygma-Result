% Domain definitions
day(mon; tue; wed; thu; fri).
cookie(oatmeal; peanut; sugar).
batch(1; 2; 3).

% Each batch of each cookie is assigned to exactly one day
1 { assigned(C, B, D) : day(D) } 1 :- cookie(C), batch(B).

% Constraint 1: No two batches of same cookie on same day
:- assigned(C, B1, D), assigned(C, B2, D), B1 != B2.

% Constraint 2: At least one batch on Monday
batch_on_day(mon) :- assigned(_, _, mon).
:- not batch_on_day(mon).

% Constraint 3: Second oatmeal batch = first peanut butter batch (same day)
assigned(peanut, 1, D) :- assigned(oatmeal, 2, D).
assigned(oatmeal, 2, D) :- assigned(peanut, 1, D).

% Constraint 4: Second sugar batch = Thursday
assigned(sugar, 2, thu).

% Additional condition: Exactly one batch on Friday
batches_on_day(D, N) :- day(D), N = #count{C,B : assigned(C,B,D)}.
:- batches_on_day(fri, N), N != 1.

% Force option A to be true
assigned(sugar, 1, mon).

#show assigned/3.