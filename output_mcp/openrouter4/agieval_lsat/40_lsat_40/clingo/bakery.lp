%% Domain
day(monday; tuesday; wednesday; thursday; friday).
kind(oatmeal; peanut_butter; sugar).
batch_num(1;2;3).

%% Day ordering for chronological constraints
day_order(monday, 1). day_order(tuesday, 2). day_order(wednesday, 3). day_order(thursday, 4). day_order(friday, 5).

%% Each batch is assigned to exactly one day
1 { made_on(K, N, D) : day(D) } 1 :- kind(K), batch_num(N).

%% Constraint 1: No two batches of same kind on same day
:- kind(K), day(D), batch_num(N1), batch_num(N2), N1 < N2, made_on(K, N1, D), made_on(K, N2, D).

%% Chronological ordering: for same kind, batches must be in order
%% Since no two same-kind batches on same day, N+1 must be strictly after N
:- kind(K), batch_num(N), N < 3, made_on(K, N, D1), made_on(K, N+1, D2), day_order(D1, O1), day_order(D2, O2), O1 >= O2.

%% Constraint 2: At least one batch on Monday
:- { made_on(K, N, monday) } = 0.

%% Constraint 3: Second batch of oatmeal is same day as first batch of peanut butter
:- made_on(oatmeal, 2, D1), made_on(peanut_butter, 1, D2), D1 != D2.

%% Constraint 4: Second batch of sugar is on Thursday
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

%% Show all assignments for debugging
#show made_on/3.
#show batches_on_day/2.
#show option_a_true/0.
#show option_b_true/0.
#show option_c_true/0.
#show option_d_true/0.
#show option_e_true/0.