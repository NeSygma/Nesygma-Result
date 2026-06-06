% Days of the week
day(monday; tuesday; wednesday; thursday; friday).

% Cookie types
cookie(oatmeal; peanut_butter; sugar).

% Batch numbers
batch(1; 2; 3).

% Given: first batch of peanut butter is on Tuesday
batch_day(peanut_butter, 1, tuesday).

% Constraint: No two batches of the same kind on the same day
:- batch_day(C, B1, D), batch_day(C, B2, D), B1 != B2.

% Constraint: At least one batch on Monday
:- not batch_day(_, _, monday).

% Constraint: Second batch of oatmeal is on same day as first batch of peanut butter
batch_day(oatmeal, 2, D) :- batch_day(peanut_butter, 1, D).

% Constraint: Second batch of sugar is on Thursday
batch_day(sugar, 2, thursday).

% Choice rule for other batches
{ batch_day(C, B, D) : cookie(C), batch(B), day(D) } :- cookie(C), batch(B), not batch_day(C, B, _).

% Ensure all batches are assigned
:- cookie(C), batch(B), not batch_day(C, B, _).

% Define when each option condition is possible

% (A) Two different kinds of cookie have their first batch made on Monday.
possible_a :- cookie(C1), cookie(C2), C1 != C2, batch_day(C1, 1, monday), batch_day(C2, 1, monday).

% (B) Two different kinds of cookie have their first batch made on Tuesday.
possible_b :- cookie(C1), cookie(C2), C1 != C2, batch_day(C1, 1, tuesday), batch_day(C2, 1, tuesday).

% (C) Two different kinds of cookie have their second batch made on Wednesday.
possible_c :- cookie(C1), cookie(C2), C1 != C2, batch_day(C1, 2, wednesday), batch_day(C2, 2, wednesday).

% (D) Two different kinds of cookie have their second batch made on Thursday.
possible_d :- cookie(C1), cookie(C2), C1 != C2, batch_day(C1, 2, thursday), batch_day(C2, 2, thursday).

% (E) Two different kinds of cookie have their third batch made on Friday.
possible_e :- cookie(C1), cookie(C2), C1 != C2, batch_day(C1, 3, friday), batch_day(C2, 3, friday).

% The correct answer is the option that is NOT possible
% So, if possible_a is false, then option(a) is true (meaning A is the EXCEPT answer)
option(a) :- not possible_a.
option(b) :- not possible_b.
option(c) :- not possible_c.
option(d) :- not possible_d.
option(e) :- not possible_e.

#show option/1.