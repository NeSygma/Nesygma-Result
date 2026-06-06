%% Problem: Bakery cookie scheduling
%% Days: Monday through Friday
day(mon; tue; wed; thu; fri).

%% Cookie kinds: oatmeal, peanut butter, sugar
kind(oatmeal; peanut_butter; sugar).

%% Each kind has exactly 3 batches (first, second, third)
batch(1..3).

%% For each kind and batch, assign a day
{ batch_day(Kind, Batch, Day) : day(Day) } 1 :- kind(Kind), batch(Batch).

%% Exactly 3 batches per kind (already enforced by 1 assignment per batch)
%% No two batches of same kind on same day
:- kind(K), day(D), batch(B1), batch(B2), B1 != B2, batch_day(K, B1, D), batch_day(K, B2, D).

%% At least one batch on Monday
:- not batch_day(_, _, mon).

%% The second batch of oatmeal cookies is made on the same day as the first batch of peanut butter cookies
:- batch_day(oatmeal, 2, D1), batch_day(peanut_butter, 1, D2), D1 != D2.

%% The second batch of sugar cookies is made on Thursday
batch_day(sugar, 2, thu).

%% Now encode each answer choice as a candidate schedule

%% Option A: oatmeal: Mon, Wed, Thu; peanut butter: Wed, Thu, Fri; sugar: Mon, Thu, Fri
candidate_a :- 
    batch_day(oatmeal, 1, mon), batch_day(oatmeal, 2, wed), batch_day(oatmeal, 3, thu),
    batch_day(peanut_butter, 1, wed), batch_day(peanut_butter, 2, thu), batch_day(peanut_butter, 3, fri),
    batch_day(sugar, 1, mon), batch_day(sugar, 2, thu), batch_day(sugar, 3, fri).

%% Option B: oatmeal: Mon, Tue, Thu; peanut butter: Tue, Wed, Thu; sugar: Mon, Wed, Thu
candidate_b :-
    batch_day(oatmeal, 1, mon), batch_day(oatmeal, 2, tue), batch_day(oatmeal, 3, thu),
    batch_day(peanut_butter, 1, tue), batch_day(peanut_butter, 2, wed), batch_day(peanut_butter, 3, thu),
    batch_day(sugar, 1, mon), batch_day(sugar, 2, wed), batch_day(sugar, 3, thu).

%% Option C: oatmeal: Tue, Wed, Thu; peanut butter: Wed, Thu, Fri; sugar: Tue, Thu, Fri
candidate_c :-
    batch_day(oatmeal, 1, tue), batch_day(oatmeal, 2, wed), batch_day(oatmeal, 3, thu),
    batch_day(peanut_butter, 1, wed), batch_day(peanut_butter, 2, thu), batch_day(peanut_butter, 3, fri),
    batch_day(sugar, 1, tue), batch_day(sugar, 2, thu), batch_day(sugar, 3, fri).

%% Option D: oatmeal: Mon, Tue, Thu; peanut butter: Mon, Wed, Thu; sugar: Mon, Thu, Fri
candidate_d :-
    batch_day(oatmeal, 1, mon), batch_day(oatmeal, 2, tue), batch_day(oatmeal, 3, thu),
    batch_day(peanut_butter, 1, mon), batch_day(peanut_butter, 2, wed), batch_day(peanut_butter, 3, thu),
    batch_day(sugar, 1, mon), batch_day(sugar, 2, thu), batch_day(sugar, 3, fri).

%% Option E: oatmeal: Mon, Thu, Fri; peanut butter: Tue, Wed, Thu; sugar: Mon, Thu, Fri
candidate_e :-
    batch_day(oatmeal, 1, mon), batch_day(oatmeal, 2, thu), batch_day(oatmeal, 3, fri),
    batch_day(peanut_butter, 1, tue), batch_day(peanut_butter, 2, wed), batch_day(peanut_butter, 3, thu),
    batch_day(sugar, 1, mon), batch_day(sugar, 2, thu), batch_day(sugar, 3, fri).

%% Map to answer
option(a) :- candidate_a.
option(b) :- candidate_b.
option(c) :- candidate_c.
option(d) :- candidate_d.
option(e) :- candidate_e.

%% Ensure exactly one option is selected
:- not 1 { option(a; b; c; d; e) } 1.

#show option/1.