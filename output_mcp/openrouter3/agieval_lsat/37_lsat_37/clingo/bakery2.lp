% Days
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).

% Cookie types
type(oatmeal). type(peanut_butter). type(sugar).

% Batches (1, 2, 3 for each type)
batch(1). batch(2). batch(3).

% For each option, we'll encode the specific assignment and check constraints
% We'll use a predicate option_assignment(Type, Batch, Day, Option)

% Option A assignment
option_assignment(oatmeal, 1, monday, a).
option_assignment(oatmeal, 2, wednesday, a).
option_assignment(oatmeal, 3, thursday, a).
option_assignment(peanut_butter, 1, wednesday, a).
option_assignment(peanut_butter, 2, thursday, a).
option_assignment(peanut_butter, 3, friday, a).
option_assignment(sugar, 1, monday, a).
option_assignment(sugar, 2, thursday, a).
option_assignment(sugar, 3, friday, a).

% Option B assignment
option_assignment(oatmeal, 1, monday, b).
option_assignment(oatmeal, 2, tuesday, b).
option_assignment(oatmeal, 3, thursday, b).
option_assignment(peanut_butter, 1, tuesday, b).
option_assignment(peanut_butter, 2, wednesday, b).
option_assignment(peanut_butter, 3, thursday, b).
option_assignment(sugar, 1, monday, b).
option_assignment(sugar, 2, wednesday, b).
option_assignment(sugar, 3, thursday, b).

% Option C assignment
option_assignment(oatmeal, 1, tuesday, c).
option_assignment(oatmeal, 2, wednesday, c).
option_assignment(oatmeal, 3, thursday, c).
option_assignment(peanut_butter, 1, wednesday, c).
option_assignment(peanut_butter, 2, thursday, c).
option_assignment(peanut_butter, 3, friday, c).
option_assignment(sugar, 1, tuesday, c).
option_assignment(sugar, 2, thursday, c).
option_assignment(sugar, 3, friday, c).

% Option D assignment
option_assignment(oatmeal, 1, monday, d).
option_assignment(oatmeal, 2, tuesday, d).
option_assignment(oatmeal, 3, thursday, d).
option_assignment(peanut_butter, 1, monday, d).
option_assignment(peanut_butter, 2, wednesday, d).
option_assignment(peanut_butter, 3, thursday, d).
option_assignment(sugar, 1, monday, d).
option_assignment(sugar, 2, thursday, d).
option_assignment(sugar, 3, friday, d).

% Option E assignment
option_assignment(oatmeal, 1, monday, e).
option_assignment(oatmeal, 2, thursday, e).
option_assignment(oatmeal, 3, friday, e).
option_assignment(peanut_butter, 1, tuesday, e).
option_assignment(peanut_butter, 2, wednesday, e).
option_assignment(peanut_butter, 3, thursday, e).
option_assignment(sugar, 1, monday, e).
option_assignment(sugar, 2, thursday, e).
option_assignment(sugar, 3, friday, e).

% Check constraints for each option
% Constraint 1: No two batches of same type on same day
invalid_option(Option) :- option_assignment(Type, Batch1, Day, Option),
                          option_assignment(Type, Batch2, Day, Option),
                          Batch1 != Batch2.

% Constraint 2: At least one batch on Monday
invalid_option(Option) :- not option_assignment(_, _, monday, Option).

% Constraint 3: Second oatmeal batch = first peanut butter batch (same day)
invalid_option(Option) :- option_assignment(oatmeal, 2, Day, Option),
                          option_assignment(peanut_butter, 1, OtherDay, Option),
                          Day != OtherDay.

% Constraint 4: Second sugar batch is on Thursday
invalid_option(Option) :- option_assignment(sugar, 2, Day, Option),
                          Day != thursday.

% Option is valid if not invalid
valid_option(Option) :- option(Option), not invalid_option(Option).

% Define which options exist
option(a). option(b). option(c). option(d). option(e).

% Map the correct answer to option/1
option(a) :- valid_option(a).
option(b) :- valid_option(b).
option(c) :- valid_option(c).
option(d) :- valid_option(d).
option(e) :- valid_option(e).

#show option/1.