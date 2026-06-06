% Cookie types
type(oatmeal).
type(peanut_butter).
type(sugar).

% Days of week (Monday-Friday)
day(monday).
day(tuesday).
day(wednesday).
day(thursday).
day(friday).

% Batch numbers (1-3)
batch_num(1).
batch_num(2).
batch_num(3).

% Each batch is made on exactly one day
1 { batch(T, B, D) : day(D) } 1 :- type(T), batch_num(B).

% No two batches of same type on same day
:- batch(T, B1, D), batch(T, B2, D), B1 != B2.

% At least one batch on Monday
:- not batch(_, _, monday).

% Second oatmeal batch = first peanut butter batch (same day)
:- batch(oatmeal, 2, D), batch(peanut_butter, 1, D2), D != D2.

% Second sugar batch is on Thursday
:- batch(sugar, 2, D), D != thursday.

% Additional condition: No batch on Wednesday
:- batch(_, _, wednesday).

% Helper predicates for counting batches per day
batches_on_day(D, N) :- day(D), N = #count{T, B : batch(T, B, D)}.

% Answer choice conditions
% (A) Exactly three batches of cookies are made on Tuesday
condition_a :- batches_on_day(tuesday, 3).

% (B) Exactly three batches of cookies are made on Friday
condition_b :- batches_on_day(friday, 3).

% (C) At least two batches of cookies are made on Monday
condition_c :- batches_on_day(monday, N), N >= 2.

% (D) At least two batches of cookies are made on Thursday
condition_d :- batches_on_day(thursday, N), N >= 2.

% (E) Fewer batches of cookies are made on Monday than on Tuesday
condition_e :- batches_on_day(monday, M), batches_on_day(tuesday, T), M < T.

% To find which condition MUST be true, we need to check if the condition
% is true in ALL valid models. We can do this by checking if the negation
% of the condition leads to unsatisfiability when combined with the constraints.

% For each option, we'll create a separate check:
% If adding "not condition_X" makes the problem unsatisfiable, then condition_X must be true.

% Check for option A: If we add "not condition_a" and it's still satisfiable, then A is not necessarily true
% We'll use a separate predicate to track if each condition is necessarily true
necessary_a :- not possible_not_a.
necessary_b :- not possible_not_b.
necessary_c :- not possible_not_c.
necessary_d :- not possible_not_d.
necessary_e :- not possible_not_e.

% Check if it's possible to have a valid schedule where condition_a is false
possible_not_a :- batch(oatmeal, 2, D), batch(peanut_butter, 1, D), batch(sugar, 2, thursday), not batch(_, _, wednesday), not condition_a.
possible_not_b :- batch(oatmeal, 2, D), batch(peanut_butter, 1, D), batch(sugar, 2, thursday), not batch(_, _, wednesday), not condition_b.
possible_not_c :- batch(oatmeal, 2, D), batch(peanut_butter, 1, D), batch(sugar, 2, thursday), not batch(_, _, wednesday), not condition_c.
possible_not_d :- batch(oatmeal, 2, D), batch(peanut_butter, 1, D), batch(sugar, 2, thursday), not batch(_, _, wednesday), not condition_d.
possible_not_e :- batch(oatmeal, 2, D), batch(peanut_butter, 1, D), batch(sugar, 2, thursday), not batch(_, _, wednesday), not condition_e.

% Map to options: The option that is necessarily true is the one that must be true
option(a) :- necessary_a.
option(b) :- necessary_b.
option(c) :- necessary_c.
option(d) :- necessary_d.
option(e) :- necessary_e.

% Show the options
#show option/1.