% Days
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).

% Cookie types
type(oatmeal). type(peanut_butter). type(sugar).

% Batches (1, 2, 3 for each type)
batch(1). batch(2). batch(3).

% Choice rule: assign each batch to a day
{ made(Type, Batch, Day) : day(Day) } 1 :- type(Type), batch(Batch).

% Constraint 1: No two batches of same type on same day
:- made(Type, Batch1, Day), made(Type, Batch2, Day), Batch1 != Batch2.

% Constraint 2: At least one batch on Monday
:- not made(_, _, monday).

% Constraint 3: Second oatmeal batch = first peanut butter batch (same day)
:- made(oatmeal, 2, Day), made(peanut_butter, 1, OtherDay), Day != OtherDay.

% Constraint 4: Second sugar batch is on Thursday
:- made(sugar, 2, Day), Day != thursday.

% Helper: count batches per type per day (for debugging)
% batches_on_day(Type, Day, N) :- N = #count{ Batch : made(Type, Batch, Day) }.

% Now evaluate each answer choice
% For each choice, we need to check if the assignment matches exactly

% Option A: oatmeal: Monday, Wednesday, Thursday; peanut butter: Wednesday, Thursday, Friday; sugar: Monday, Thursday, Friday
% This means: oatmeal batches on Mon, Wed, Thu; peanut butter on Wed, Thu, Fri; sugar on Mon, Thu, Fri
% We need to check if there exists an assignment that matches this pattern

% For option A to be valid, we need to check if the days match the pattern
% But we need to consider that batches are indistinguishable except for order
% Actually, the problem asks for "complete and accurate list of the days"
% So we need to check if the set of days for each type matches exactly

% Let's define the expected days for each option
expected_days(oatmeal, a, monday). expected_days(oatmeal, a, wednesday). expected_days(oatmeal, a, thursday).
expected_days(peanut_butter, a, wednesday). expected_days(peanut_butter, a, thursday). expected_days(peanut_butter, a, friday).
expected_days(sugar, a, monday). expected_days(sugar, a, thursday). expected_days(sugar, a, friday).

expected_days(oatmeal, b, monday). expected_days(oatmeal, b, tuesday). expected_days(oatmeal, b, thursday).
expected_days(peanut_butter, b, tuesday). expected_days(peanut_butter, b, wednesday). expected_days(peanut_butter, b, thursday).
expected_days(sugar, b, monday). expected_days(sugar, b, wednesday). expected_days(sugar, b, thursday).

expected_days(oatmeal, c, tuesday). expected_days(oatmeal, c, wednesday). expected_days(oatmeal, c, thursday).
expected_days(peanut_butter, c, wednesday). expected_days(peanut_butter, c, thursday). expected_days(peanut_butter, c, friday).
expected_days(sugar, c, tuesday). expected_days(sugar, c, thursday). expected_days(sugar, c, friday).

expected_days(oatmeal, d, monday). expected_days(oatmeal, d, tuesday). expected_days(oatmeal, d, thursday).
expected_days(peanut_butter, d, monday). expected_days(peanut_butter, d, wednesday). expected_days(peanut_butter, d, thursday).
expected_days(sugar, d, monday). expected_days(sugar, d, thursday). expected_days(sugar, d, friday).

expected_days(oatmeal, e, monday). expected_days(oatmeal, e, thursday). expected_days(oatmeal, e, friday).
expected_days(peanut_butter, e, tuesday). expected_days(peanut_butter, e, wednesday). expected_days(peanut_butter, e, thursday).
expected_days(sugar, e, monday). expected_days(sugar, e, thursday). expected_days(sugar, e, friday).

% Check if the assignment matches the expected days for each option
% For each type and option, count how many batches are on expected days
% and ensure all batches are on expected days and no extra days

% Helper: actual days used for each type
actual_day(Type, Day) :- made(Type, _, Day).

% For option A: check if actual days match expected days
option_a_valid :- 
    % For oatmeal
    actual_day(oatmeal, monday), actual_day(oatmeal, wednesday), actual_day(oatmeal, thursday),
    not actual_day(oatmeal, tuesday), not actual_day(oatmeal, friday),
    % For peanut butter
    actual_day(peanut_butter, wednesday), actual_day(peanut_butter, thursday), actual_day(peanut_butter, friday),
    not actual_day(peanut_butter, monday), not actual_day(peanut_butter, tuesday),
    % For sugar
    actual_day(sugar, monday), actual_day(sugar, thursday), actual_day(sugar, friday),
    not actual_day(sugar, tuesday), not actual_day(sugar, wednesday).

% Similarly for other options
option_b_valid :-
    actual_day(oatmeal, monday), actual_day(oatmeal, tuesday), actual_day(oatmeal, thursday),
    not actual_day(oatmeal, wednesday), not actual_day(oatmeal, friday),
    actual_day(peanut_butter, tuesday), actual_day(peanut_butter, wednesday), actual_day(peanut_butter, thursday),
    not actual_day(peanut_butter, monday), not actual_day(peanut_butter, friday),
    actual_day(sugar, monday), actual_day(sugar, wednesday), actual_day(sugar, thursday),
    not actual_day(sugar, tuesday), not actual_day(sugar, friday).

option_c_valid :-
    actual_day(oatmeal, tuesday), actual_day(oatmeal, wednesday), actual_day(oatmeal, thursday),
    not actual_day(oatmeal, monday), not actual_day(oatmeal, friday),
    actual_day(peanut_butter, wednesday), actual_day(peanut_butter, thursday), actual_day(peanut_butter, friday),
    not actual_day(peanut_butter, monday), not actual_day(peanut_butter, tuesday),
    actual_day(sugar, tuesday), actual_day(sugar, thursday), actual_day(sugar, friday),
    not actual_day(sugar, monday), not actual_day(sugar, wednesday).

option_d_valid :-
    actual_day(oatmeal, monday), actual_day(oatmeal, tuesday), actual_day(oatmeal, thursday),
    not actual_day(oatmeal, wednesday), not actual_day(oatmeal, friday),
    actual_day(peanut_butter, monday), actual_day(peanut_butter, wednesday), actual_day(peanut_butter, thursday),
    not actual_day(peanut_butter, tuesday), not actual_day(peanut_butter, friday),
    actual_day(sugar, monday), actual_day(sugar, thursday), actual_day(sugar, friday),
    not actual_day(sugar, tuesday), not actual_day(sugar, wednesday).

option_e_valid :-
    actual_day(oatmeal, monday), actual_day(oatmeal, thursday), actual_day(oatmeal, friday),
    not actual_day(oatmeal, tuesday), not actual_day(oatmeal, wednesday),
    actual_day(peanut_butter, tuesday), actual_day(peanut_butter, wednesday), actual_day(peanut_butter, thursday),
    not actual_day(peanut_butter, monday), not actual_day(peanut_butter, friday),
    actual_day(sugar, monday), actual_day(sugar, thursday), actual_day(sugar, friday),
    not actual_day(sugar, tuesday), not actual_day(sugar, wednesday).

% Map the correct answer to option/1
option(a) :- option_a_valid.
option(b) :- option_b_valid.
option(c) :- option_c_valid.
option(d) :- option_d_valid.
option(e) :- option_e_valid.

#show option/1.