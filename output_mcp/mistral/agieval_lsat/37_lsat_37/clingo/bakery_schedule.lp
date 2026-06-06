% Days of the week
day(monday; tuesday; wednesday; thursday; friday).

% Cookie types
cookie(oatmeal; peanut_butter; sugar).

% Batch numbers
batch(1..3).

% Option A schedule (order = batch 1, 2, 3)
oatmeal_option_a(1, monday).
oatmeal_option_a(2, wednesday).
oatmeal_option_a(3, thursday).

peanut_butter_option_a(1, wednesday).
peanut_butter_option_a(2, thursday).
peanut_butter_option_a(3, friday).

sugar_option_a(1, monday).
sugar_option_a(2, thursday).
sugar_option_a(3, friday).

% Option B schedule
oatmeal_option_b(1, monday).
oatmeal_option_b(2, tuesday).
oatmeal_option_b(3, thursday).

peanut_butter_option_b(1, tuesday).
peanut_butter_option_b(2, wednesday).
peanut_butter_option_b(3, thursday).

sugar_option_b(1, monday).
sugar_option_b(2, wednesday).
sugar_option_b(3, thursday).

% Option C schedule
oatmeal_option_c(1, tuesday).
oatmeal_option_c(2, wednesday).
oatmeal_option_c(3, thursday).

peanut_butter_option_c(1, wednesday).
peanut_butter_option_c(2, thursday).
peanut_butter_option_c(3, friday).

sugar_option_c(1, tuesday).
sugar_option_c(2, thursday).
sugar_option_c(3, friday).

% Option D schedule
oatmeal_option_d(1, monday).
oatmeal_option_d(2, tuesday).
oatmeal_option_d(3, thursday).

peanut_butter_option_d(1, monday).
peanut_butter_option_d(2, wednesday).
peanut_butter_option_d(3, thursday).

sugar_option_d(1, monday).
sugar_option_d(2, thursday).
sugar_option_d(3, friday).

% Option E schedule
oatmeal_option_e(1, monday).
oatmeal_option_e(2, thursday).
oatmeal_option_e(3, friday).

peanut_butter_option_e(1, tuesday).
peanut_butter_option_e(2, wednesday).
peanut_butter_option_e(3, thursday).

sugar_option_e(1, monday).
sugar_option_e(2, thursday).
sugar_option_e(3, friday).

% Helper predicates to check if at least one batch is on Monday for each option
monday_batch_option_a :- oatmeal_option_a(_, monday).
monday_batch_option_a :- peanut_butter_option_a(_, monday).
monday_batch_option_a :- sugar_option_a(_, monday).

monday_batch_option_b :- oatmeal_option_b(_, monday).
monday_batch_option_b :- peanut_butter_option_b(_, monday).
monday_batch_option_b :- sugar_option_b(_, monday).

monday_batch_option_c :- oatmeal_option_c(_, monday).
monday_batch_option_c :- peanut_butter_option_c(_, monday).
monday_batch_option_c :- sugar_option_c(_, monday).

monday_batch_option_d :- oatmeal_option_d(_, monday).
monday_batch_option_d :- peanut_butter_option_d(_, monday).
monday_batch_option_d :- sugar_option_d(_, monday).

monday_batch_option_e :- oatmeal_option_e(_, monday).
monday_batch_option_e :- peanut_butter_option_e(_, monday).
monday_batch_option_e :- sugar_option_e(_, monday).

% Check oatmeal batch 2 = peanut_butter batch 1 for each option
oatmeal_pb_match_option_a :- oatmeal_option_a(2, D), peanut_butter_option_a(1, D).

atmeal_pb_match_option_b :- oatmeal_option_b(2, D), peanut_butter_option_b(1, D).

atmeal_pb_match_option_c :- oatmeal_option_c(2, D), peanut_butter_option_c(1, D).

atmeal_pb_match_option_d :- oatmeal_option_d(2, D), peanut_butter_option_d(1, D).

atmeal_pb_match_option_e :- oatmeal_option_e(2, D), peanut_butter_option_e(1, D).

% Check sugar batch 2 = thursday for each option
sugar_batch2_thursday_option_a :- sugar_option_a(2, thursday).
sugar_batch2_thursday_option_b :- sugar_option_b(2, thursday).
sugar_batch2_thursday_option_c :- sugar_option_c(2, thursday).
sugar_batch2_thursday_option_d :- sugar_option_d(2, thursday).
sugar_batch2_thursday_option_e :- sugar_option_e(2, thursday).

% Option A is valid if all conditions are met
option_a_valid :-
    monday_batch_option_a,
    oatmeal_pb_match_option_a,
    sugar_batch2_thursday_option_a.

% Option B is valid if all conditions are met
option_b_valid :-
    monday_batch_option_b,
    oatmeal_pb_match_option_b,
    sugar_batch2_thursday_option_b.

% Option C is valid if all conditions are met
option_c_valid :-
    monday_batch_option_c,
    oatmeal_pb_match_option_c,
    sugar_batch2_thursday_option_c.

% Option D is valid if all conditions are met
option_d_valid :-
    monday_batch_option_d,
    oatmeal_pb_match_option_d,
    sugar_batch2_thursday_option_d.

% Option E is valid if all conditions are met
option_e_valid :-
    monday_batch_option_e,
    oatmeal_pb_match_option_e,
    sugar_batch2_thursday_option_e.

% Exactly one option can be valid
:- option_a_valid, option_b_valid.
:- option_a_valid, option_c_valid.
:- option_a_valid, option_d_valid.
:- option_a_valid, option_e_valid.
:- option_b_valid, option_c_valid.
:- option_b_valid, option_d_valid.
:- option_b_valid, option_e_valid.
:- option_c_valid, option_d_valid.
:- option_c_valid, option_e_valid.
:- option_d_valid, option_e_valid.

% Map the correct answer to option/1
option(a) :- option_a_valid.
option(b) :- option_b_valid.
option(c) :- option_c_valid.
option(d) :- option_d_valid.
option(e) :- option_e_valid.

#show option/1.