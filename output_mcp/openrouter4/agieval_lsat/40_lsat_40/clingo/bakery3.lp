%% Domain
day(monday; tuesday; wednesday; thursday; friday).
kind(oatmeal; peanut_butter; sugar).
batch_num(1;2;3).

%% Day ordering
day_order(monday,1). day_order(tuesday,2). day_order(wednesday,3). day_order(thursday,4). day_order(friday,5).

%% Assign each batch to exactly one day
1 { made_on(K, N, D) : day(D) } 1 :- kind(K), batch_num(N).

%% No two batches of same kind on same day
:- kind(K), day(D), batch_num(N1), batch_num(N2), N1 < N2, made_on(K, N1, D), made_on(K, N2, D).

%% Chronological ordering for same kind
:- kind(K), batch_num(N), N < 3, made_on(K, N, D1), made_on(K, N+1, D2), day_order(D1, O1), day_order(D2, O2), O1 >= O2.

%% At least one batch on Monday
:- { made_on(K, N, monday) } = 0.

%% Second oatmeal same day as first peanut butter
:- made_on(oatmeal, 2, D1), made_on(peanut_butter, 1, D2), D1 != D2.

%% Second sugar on Thursday
made_on(sugar, 2, thursday).

%% Condition: No batch on Wednesday
:- made_on(K, N, wednesday).

%% Helper for counting batches per day
batches_on_day(D, N) :- N = #count { K, B : made_on(K, B, D) }, day(D).

%% Derive option conditions
option_a_true :- batches_on_day(tuesday, 3).
option_b_true :- batches_on_day(friday, 3).
option_c_true :- batches_on_day(monday, N), N >= 2.
option_d_true :- batches_on_day(thursday, N), N >= 2.
option_e_true :- batches_on_day(monday, M), batches_on_day(tuesday, T), M < T.

%% Map to answer choices
option(a) :- option_a_true.
option(b) :- option_b_true.
option(c) :- option_c_true.
option(d) :- option_d_true.
option(e) :- option_e_true.

#show option/1.
#show batches_on_day/2.