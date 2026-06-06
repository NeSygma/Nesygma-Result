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

%% Let's get full models to analyze
#show assigned/3.