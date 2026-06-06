%% Problem: Bakery scheduling
%% 3 kinds: oatmeal, peanut_butter, sugar
%% 3 batches of each kind (1st, 2nd, 3rd)
%% Days: Monday through Friday (1..5)

%% Domain
day(1..5).  % 1=Mon, 2=Tue, 3=Wed, 4=Thu, 5=Fri
kind(oatmeal; peanut_butter; sugar).
batch(1..3).

%% Each batch of each kind is assigned to exactly one day
{ assigned(Kind, Batch, Day) : day(Day) } 1 :- kind(Kind), batch(Batch).

%% No two batches of the same kind on the same day
:- kind(K), day(D), batch(B1), batch(B2), B1 != B2, assigned(K, B1, D), assigned(K, B2, D).

%% At least one batch on Monday
:- not assigned(_, _, 1).

%% The second batch of oatmeal cookies is made on the same day as the first batch of peanut butter cookies
:- assigned(oatmeal, 2, D1), assigned(peanut_butter, 1, D2), D1 != D2.

%% The second batch of sugar cookies is made on Thursday (day 4)
assigned(sugar, 2, 4).

%% Condition: one kind's first batch is on the same day as another kind's third batch
condition_holds :- kind(K1), kind(K2), K1 != K2, assigned(K1, 1, D), assigned(K2, 3, D).
:- not condition_holds.

%% Count batches per day
batches_on_day(D, N) :- day(D), N = #count{ K,B : assigned(K,B,D) }.

%% Option A: At least one batch on each of the five days
option_a_holds :- day(D), batches_on_day(D, N), N >= 1.
option_a_fails :- day(D), batches_on_day(D, 0).

%% Option B: At least two batches on Wednesday (day 3)
option_b_holds :- batches_on_day(3, N), N >= 2.
option_b_fails :- batches_on_day(3, N), N < 2.

%% Option C: Exactly one batch on Monday (day 1)
option_c_holds :- batches_on_day(1, 1).
option_c_fails :- batches_on_day(1, N), N != 1.

%% Option D: Exactly two batches on Tuesday (day 2)
option_d_holds :- batches_on_day(2, 2).
option_d_fails :- batches_on_day(2, N), N != 2.

%% Option E: Exactly one batch on Friday (day 5)
option_e_holds :- batches_on_day(5, 1).
option_e_fails :- batches_on_day(5, N), N != 1.

%% We need to find which option COULD BE FALSE.
%% That means: there exists a valid schedule where that option is false.
%% So we check each option: can it be false in some model?

%% For each option, we check if there's a model where it fails.
%% We'll enumerate all models and check.

#show assigned/3.
#show batches_on_day/2.
#show option_a_fails/0.
#show option_b_fails/0.
#show option_c_fails/0.
#show option_d_fails/0.
#show option_e_fails/0.