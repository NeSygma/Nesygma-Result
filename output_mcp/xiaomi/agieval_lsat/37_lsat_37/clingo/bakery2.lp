% Days of the week
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).

% Cookie types
cookie(oatmeal). cookie(peanut_butter). cookie(sugar).

% Batch numbers (1,2,3)
batch(1). batch(2). batch(3).

% Answer choices as facts
% Format: choice_batch(Cookie, Batch, Day)
% Choice A
choice_batch(a, oatmeal, 1, monday).
choice_batch(a, oatmeal, 2, wednesday).
choice_batch(a, oatmeal, 3, thursday).
choice_batch(a, peanut_butter, 1, wednesday).
choice_batch(a, peanut_butter, 2, thursday).
choice_batch(a, peanut_butter, 3, friday).
choice_batch(a, sugar, 1, monday).
choice_batch(a, sugar, 2, thursday).
choice_batch(a, sugar, 3, friday).

% Choice B
choice_batch(b, oatmeal, 1, monday).
choice_batch(b, oatmeal, 2, tuesday).
choice_batch(b, oatmeal, 3, thursday).
choice_batch(b, peanut_butter, 1, tuesday).
choice_batch(b, peanut_butter, 2, wednesday).
choice_batch(b, peanut_butter, 3, thursday).
choice_batch(b, sugar, 1, monday).
choice_batch(b, sugar, 2, wednesday).
choice_batch(b, sugar, 3, thursday).

% Choice C
choice_batch(c, oatmeal, 1, tuesday).
choice_batch(c, oatmeal, 2, wednesday).
choice_batch(c, oatmeal, 3, thursday).
choice_batch(c, peanut_butter, 1, wednesday).
choice_batch(c, peanut_butter, 2, thursday).
choice_batch(c, peanut_butter, 3, friday).
choice_batch(c, sugar, 1, tuesday).
choice_batch(c, sugar, 2, thursday).
choice_batch(c, sugar, 3, friday).

% Choice D
choice_batch(d, oatmeal, 1, monday).
choice_batch(d, oatmeal, 2, tuesday).
choice_batch(d, oatmeal, 3, thursday).
choice_batch(d, peanut_butter, 1, monday).
choice_batch(d, peanut_butter, 2, wednesday).
choice_batch(d, peanut_butter, 3, thursday).
choice_batch(d, sugar, 1, monday).
choice_batch(d, sugar, 2, thursday).
choice_batch(d, sugar, 3, friday).

% Choice E
choice_batch(e, oatmeal, 1, monday).
choice_batch(e, oatmeal, 2, thursday).
choice_batch(e, oatmeal, 3, friday).
choice_batch(e, peanut_butter, 1, tuesday).
choice_batch(e, peanut_butter, 2, wednesday).
choice_batch(e, peanut_butter, 3, thursday).
choice_batch(e, sugar, 1, monday).
choice_batch(e, sugar, 2, thursday).
choice_batch(e, sugar, 3, friday).

% Check constraints for each choice
% Constraint 1: No two batches of same type on same day
valid_no_duplicates(Choice) :- 
    choice_batch(Choice, Cookie, B1, Day),
    choice_batch(Choice, Cookie, B2, Day),
    B1 != B2.

% Constraint 2: At least one batch on Monday
valid_monday(Choice) :- 
    choice_batch(Choice, _, _, monday).

% Constraint 3: Second oatmeal = first peanut butter
valid_oatmeal_pb(Choice) :- 
    choice_batch(Choice, oatmeal, 2, Day),
    choice_batch(Choice, peanut_butter, 1, Day).

% Constraint 4: Second sugar = Thursday
valid_sugar_thursday(Choice) :- 
    choice_batch(Choice, sugar, 2, thursday).

% A choice is valid if all constraints hold
valid(Choice) :- 
    valid_no_duplicates(Choice),
    valid_monday(Choice),
    valid_oatmeal_pb(Choice),
    valid_sugar_thursday(Choice).

% Map to options
option(a) :- valid(a).
option(b) :- valid(b).
option(c) :- valid(c).
option(d) :- valid(d).
option(e) :- valid(e).

% Show all valid options
#show option/1.
#show valid/1.