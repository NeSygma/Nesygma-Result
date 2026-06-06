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

% Helper: Check if each option could be true
% Option A: First sugar batch on Monday
option_a_possible :- assigned(sugar, 1, mon).

% Option B: First oatmeal batch on Tuesday
option_b_possible :- assigned(oatmeal, 1, tue).

% Option C: Third oatmeal batch on Friday
option_c_possible :- assigned(oatmeal, 3, fri).

% Option D: First peanut butter batch on Wednesday
option_d_possible :- assigned(peanut, 1, wed).

% Option E: Second peanut butter batch on Tuesday
option_e_possible :- assigned(peanut, 2, tue).

% Map options
option(a) :- option_a_possible.
option(b) :- option_b_possible.
option(c) :- option_c_possible.
option(d) :- option_d_possible.
option(e) :- option_e_possible.

#show option/1.