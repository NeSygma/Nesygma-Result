% Domains
kind(o). kind(p). kind(s).
batch_num(1). batch_num(2). batch_num(3).
day(mon). day(tue). day(wed). day(thu). day(fri).

% Each batch of each kind is assigned to exactly one day
1 { assign(K, B, D) : day(D) } 1 :- kind(K), batch_num(B).

% Constraint 1: No two batches of same kind on same day
:- assign(K, B1, D), assign(K, B2, D), B1 != B2.

% Constraint 2: At least one batch on Monday
has_batch(D) :- assign(_, _, D).
:- not has_batch(mon).

% Constraint 3: Second oatmeal same day as first peanut butter
:- assign(o, 2, D1), assign(p, 1, D2), D1 != D2.

% Constraint 4: Second sugar on Thursday
:- assign(s, 2, D), D != thu.

% Additional condition: One kind's first batch same day as another kind's third batch
first_third :- assign(K1, 1, D), assign(K2, 3, D), K1 != K2.
:- not first_third.

% Count batches per day
batch_count(D, N) :- day(D), N = #count { K, B : assign(K, B, D) }.

% Check each option - TRUE means the statement holds
opt_a_true :- batch_count(mon, N1), N1 >= 1, batch_count(tue, N2), N2 >= 1, batch_count(wed, N3), N3 >= 1, batch_count(thu, N4), N4 >= 1, batch_count(fri, N5), N5 >= 1.
opt_b_true :- batch_count(wed, N), N >= 2.
opt_c_true :- batch_count(mon, N), N = 1.
opt_d_true :- batch_count(tue, N), N = 2.
opt_e_true :- batch_count(fri, N), N = 1.

% An option could be false if there exists a model where it's not true
opt_a_false :- not opt_a_true.
opt_b_false :- not opt_b_true.
opt_c_false :- not opt_c_true.
opt_d_false :- not opt_d_true.
opt_e_false :- not opt_e_true.

#show opt_a_false/0.
#show opt_b_false/0.
#show opt_c_false/0.
#show opt_d_false/0.
#show opt_e_false/0.
#show batch_count/2.
#show assign/3.