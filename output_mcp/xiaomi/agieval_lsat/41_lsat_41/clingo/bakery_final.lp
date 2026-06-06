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

% Check each option individually
% Option A: First sugar batch on Monday
check_a :- assigned(sugar, 1, mon).

% Option B: First oatmeal batch on Tuesday
check_b :- assigned(oatmeal, 1, tue).

% Option C: Third oatmeal batch on Friday
check_c :- assigned(oatmeal, 3, fri).

% Option D: First peanut butter batch on Wednesday
check_d :- assigned(peanut, 1, wed).

% Option E: Second peanut butter batch on Tuesday
check_e :- assigned(peanut, 2, tue).

% Show which options are possible
option(a) :- check_a.
option(b) :- check_b.
option(c) :- check_c.
option(d) :- check_d.
option(e) :- check_e.

% Force at least one option to be true
:- not option(a), not option(b), not option(c), not option(d), not option(e).

#show option/1.