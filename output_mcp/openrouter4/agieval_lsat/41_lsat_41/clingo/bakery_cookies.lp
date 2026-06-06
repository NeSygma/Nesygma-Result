% Domains
day(monday; tuesday; wednesday; thursday; friday).
type(oatmeal; peanut_butter; sugar).
batch(1..3).  % 1=first, 2=second, 3=third

% Each batch is assigned to exactly one day
1 { assigned(T, B, D) : day(D) } 1 :- type(T), batch(B).

% Condition 1: No two batches of the same kind on the same day
:- type(T), day(D), #count{B : assigned(T, B, D)} > 1.

% Condition 2: At least one batch on Monday
:- not #count{T,B : assigned(T, B, monday)} >= 1.

% Condition 3: Second oatmeal = first peanut butter day
:- assigned(oatmeal, 2, D1), assigned(peanut_butter, 1, D2), D1 != D2.

% Condition 4: Second sugar on Thursday
assigned(sugar, 2, thursday).

% Extra condition: Exactly one batch on Friday
:- #count{T,B : assigned(T, B, friday)} != 1.

% Option conditions
a_possible :- assigned(sugar, 1, monday).
b_possible :- assigned(oatmeal, 1, tuesday).
c_possible :- assigned(oatmeal, 3, friday).
d_possible :- assigned(peanut_butter, 1, wednesday).
e_possible :- assigned(peanut_butter, 2, tuesday).

% Choose exactly one option to test
1 { test_option(a); test_option(b); test_option(c); test_option(d); test_option(e) } 1.

% If we test an option, it must be true in this model
:- test_option(a), not a_possible.
:- test_option(b), not b_possible.
:- test_option(c), not c_possible.
:- test_option(d), not d_possible.
:- test_option(e), not e_possible.

% Map to required output format
option(a) :- test_option(a).
option(b) :- test_option(b).
option(c) :- test_option(c).
option(d) :- test_option(d).
option(e) :- test_option(e).

#show option/1.