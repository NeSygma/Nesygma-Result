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

% Map the correct answer to option/1 (MANDATORY)
% We need to find which condition MUST be true in ALL valid models
% Since we're looking for what MUST be true, we need to check if the condition
% holds in every valid model. In ASP, we can do this by checking if the
% negation leads to unsatisfiability.

% For "must be true", we check if the condition is true in all models
% We'll use a different approach: check if the condition is false leads to unsat
% But since we can't easily do that in one file, we'll use a different method:
% We'll check which conditions are true in the current model, and since we're
% looking for what MUST be true, we need to ensure our model is complete.

% Actually, let's think differently: We need to find which statement is logically
% necessary given the constraints. We can check each condition by seeing if
% its negation is compatible with the constraints.

% Let's create separate checks for each option
% For each option, we'll check if the option's condition is necessarily true

% We'll use a different approach: enumerate all possible valid schedules
% and see which conditions hold in all of them.

% First, let's find all valid schedules
valid_schedule :- batch(oatmeal, 2, D), batch(peanut_butter, 1, D), batch(sugar, 2, thursday).

% Now check each condition across all valid schedules
% We'll use a helper to mark which conditions are always true

% For option A: Check if in all valid schedules, Tuesday has exactly 3 batches
always_a :- valid_schedule, condition_a.
% But we need to check if there exists any valid schedule where condition_a is false
% If yes, then A is not necessarily true

% Let's use a different approach: We'll check each option by seeing if
% its negation is compatible with the constraints

% For option A: Is it possible to have a valid schedule where Tuesday does NOT have exactly 3 batches?
possible_not_a :- valid_schedule, not condition_a.
% If possible_not_a is true, then A is not necessarily true

% Similarly for other options
possible_not_b :- valid_schedule, not condition_b.
possible_not_c :- valid_schedule, not condition_c.
possible_not_d :- valid_schedule, not condition_d.
possible_not_e :- valid_schedule, not condition_e.

% Now map to options: The option that is NOT possible to be false is the one that must be true
option(a) :- not possible_not_a.
option(b) :- not possible_not_b.
option(c) :- not possible_not_c.
option(d) :- not possible_not_d.
option(e) :- not possible_not_e.

% Show the options
#show option/1.
#show batch/3.
#show batches_on_day/2.