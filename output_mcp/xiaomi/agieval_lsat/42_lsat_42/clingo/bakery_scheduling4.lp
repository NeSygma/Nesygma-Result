% Domains
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).
cookie(oatmeal). cookie(peanut_butter). cookie(sugar).
batch(1). batch(2). batch(3).

% Each batch of each cookie is assigned to exactly one day
1 { assign(C, B, D) : day(D) } 1 :- cookie(C), batch(B).

% No two batches of the same kind on the same day
:- assign(C, B1, D), assign(C, B2, D), B1 != B2.

% At least one batch on Monday
:- not assign(_, _, monday).

% Second oatmeal batch = first peanut butter batch (same day)
assign(oatmeal, 2, D) :- assign(peanut_butter, 1, D).
assign(peanut_butter, 1, D) :- assign(oatmeal, 2, D).

% Second sugar batch = Thursday
assign(sugar, 2, thursday).

% Additional condition: One kind's first batch = another kind's third batch
first_third_same_day :- assign(C1, 1, D), assign(C2, 3, D), C1 != C2.

% We need to consider all valid assignments that satisfy the additional condition
valid_assignment :- first_third_same_day.

% Count batches per day
batches_on_day(D, N) :- day(D), N = #count{C,B : assign(C,B,D)}.

% Evaluate each option
% Option A: At least one batch on each of the five days
all_days_have_batch :- batches_on_day(monday, N1), N1 >= 1,
                       batches_on_day(tuesday, N2), N2 >= 1,
                       batches_on_day(wednesday, N3), N3 >= 1,
                       batches_on_day(thursday, N4), N4 >= 1,
                       batches_on_day(friday, N5), N5 >= 1.

% Option B: At least two batches on Wednesday
option_b_true :- batches_on_day(wednesday, N), N >= 2.

% Option C: Exactly one batch on Monday
option_c_true :- batches_on_day(monday, 1).

% Option D: Exactly two batches on Tuesday
option_d_true :- batches_on_day(tuesday, 2).

% Option E: Exactly one batch on Friday
option_e_true :- batches_on_day(friday, 1).

% Check if each option is necessarily true (true in ALL valid assignments)
% We'll use a different approach: find assignments where each option is false
% and see which ones are possible

% For each option, check if it can be false
option_a_can_be_false :- valid_assignment, not all_days_have_batch.
option_b_can_be_false :- valid_assignment, not option_b_true.
option_c_can_be_false :- valid_assignment, not option_c_true.
option_d_can_be_false :- valid_assignment, not option_d_true.
option_e_can_be_false :- valid_assignment, not option_e_true.

% The answer is the option that could be false (i.e., not necessarily true)
option(a) :- option_a_can_be_false.
option(b) :- option_b_can_be_false.
option(c) :- option_c_can_be_false.
option(d) :- option_d_can_be_false.
option(e) :- option_e_can_be_false.

#show option/1.