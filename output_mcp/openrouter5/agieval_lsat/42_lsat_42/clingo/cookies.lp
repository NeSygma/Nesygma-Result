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

%% Additional condition from the question:
%% "If one kind of cookie's first batch is made on the same day as another kind of cookie's third batch"
%% We need to find which option COULD BE FALSE under this condition.
%% So we need to consider all schedules that satisfy the condition, and see which options are not necessarily true.

%% Let's define the condition: there exist kinds K1, K2 (different) such that first batch of K1 is on same day as third batch of K2.
condition_holds :- kind(K1), kind(K2), K1 != K2, assigned(K1, 1, D), assigned(K2, 3, D).

%% We only consider schedules where condition_holds is true
:- not condition_holds.

%% Now evaluate each option:

%% (A) At least one batch of cookies is made on each of the five days.
option_a_true :- day(D), assigned(_, _, D).  % This is per-day, need to check all days
% Actually: option A is "at least one batch on each day"
% So A is false if there exists a day with no batches
a_false :- day(D), not assigned(_, _, D).
option_a_possible_false :- a_false.

%% (B) At least two batches of cookies are made on Wednesday (day 3).
b_false :- { assigned(_, _, 3) } <= 1.
option_b_possible_false :- b_false.

%% (C) Exactly one batch of cookies is made on Monday (day 1).
c_false :- { assigned(_, _, 1) } != 1.
option_c_possible_false :- c_false.

%% (D) Exactly two batches of cookies are made on Tuesday (day 2).
d_false :- { assigned(_, _, 2) } != 2.
option_d_possible_false :- d_false.

%% (E) Exactly one batch of cookies is made on Friday (day 5).
e_false :- { assigned(_, _, 5) } != 1.
option_e_possible_false :- e_false.

%% The question asks: which one COULD BE FALSE?
%% So we need to find which option has a model where it is false.
%% Since we are in SAT mode, we can check each option by seeing if there exists
%% a model where that option is false.

%% We'll use a choice to pick which option to test for falsifiability
%% But simpler: we can just enumerate all models and see.

%% Actually, let's use a different approach. We'll use #show to see all models
%% and then determine which option can be false.

#show assigned/3.
#show option_a_possible_false/0.
#show option_b_possible_false/0.
#show option_c_possible_false/0.
#show option_d_possible_false/0.
#show option_e_possible_false/0.