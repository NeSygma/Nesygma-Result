% Domains
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).
kind(oatmeal). kind(pb). kind(sugar).
batch(1). batch(2). batch(3).

% Each batch must be assigned to exactly one day
1 { schedule(K, B, D) : day(D) } 1 :- kind(K), batch(B).

% Constraint 1: No two batches of the same kind on the same day
:- schedule(K, B1, D), schedule(K, B2, D), B1 != B2.

% Constraint 2: At least one batch on Monday
made_on_monday :- schedule(_, _, monday).
:- not made_on_monday.

% Constraint 3: Second batch of oatmeal same day as first batch of peanut butter
:- schedule(oatmeal, 2, D1), schedule(pb, 1, D2), D1 != D2.

% Constraint 4: Second batch of sugar is Thursday
:- schedule(sugar, 2, D), D != thursday.

% Now encode each answer option as candidate facts
% Option A: oatmeal: Mon, Wed, Thu; pb: Wed, Thu, Fri; sugar: Mon, Thu, Fri
oa_a(oatmeal, 1, monday). oa_a(oatmeal, 2, wednesday). oa_a(oatmeal, 3, thursday).
oa_a(pb, 1, wednesday). oa_a(pb, 2, thursday). oa_a(pb, 3, friday).
oa_a(sugar, 1, monday). oa_a(sugar, 2, thursday). oa_a(sugar, 3, friday).

% Option B: oatmeal: Mon, Tue, Thu; pb: Tue, Wed, Thu; sugar: Mon, Wed, Thu
oa_b(oatmeal, 1, monday). oa_b(oatmeal, 2, tuesday). oa_b(oatmeal, 3, thursday).
oa_b(pb, 1, tuesday). oa_b(pb, 2, wednesday). oa_b(pb, 3, thursday).
oa_b(sugar, 1, monday). oa_b(sugar, 2, wednesday). oa_b(sugar, 3, thursday).

% Option C: oatmeal: Tue, Wed, Thu; pb: Wed, Thu, Fri; sugar: Tue, Thu, Fri
oa_c(oatmeal, 1, tuesday). oa_c(oatmeal, 2, wednesday). oa_c(oatmeal, 3, thursday).
oa_c(pb, 1, wednesday). oa_c(pb, 2, thursday). oa_c(pb, 3, friday).
oa_c(sugar, 1, tuesday). oa_c(sugar, 2, thursday). oa_c(sugar, 3, friday).

% Option D: oatmeal: Mon, Tue, Thu; pb: Mon, Wed, Thu; sugar: Mon, Thu, Fri
oa_d(oatmeal, 1, monday). oa_d(oatmeal, 2, tuesday). oa_d(oatmeal, 3, thursday).
oa_d(pb, 1, monday). oa_d(pb, 2, wednesday). oa_d(pb, 3, thursday).
oa_d(sugar, 1, monday). oa_d(sugar, 2, thursday). oa_d(sugar, 3, friday).

% Option E: oatmeal: Mon, Thu, Fri; pb: Tue, Wed, Thu; sugar: Mon, Thu, Fri
oa_e(oatmeal, 1, monday). oa_e(oatmeal, 2, thursday). oa_e(oatmeal, 3, friday).
oa_e(pb, 1, tuesday). oa_e(pb, 2, wednesday). oa_e(pb, 3, thursday).
oa_e(sugar, 1, monday). oa_e(sugar, 2, thursday). oa_e(sugar, 3, friday).

% Check each option against constraints
% Option A: oatmeal2=wednesday, pb1=wednesday -> same day OK. sugar2=thursday OK. Monday has oatmeal1 and sugar1 -> OK.
% But need to check: no two same kind on same day - all distinct per kind? Yes.
% Option A satisfies all constraints.

% Option B: oatmeal2=tuesday, pb1=tuesday -> same day OK. sugar2=wednesday -> FAILS constraint 4 (must be thursday).

% Option C: oatmeal2=wednesday, pb1=wednesday -> same day OK. sugar2=thursday OK. But no batch on Monday -> FAILS constraint 2.

% Option D: oatmeal2=tuesday, pb1=monday -> NOT same day -> FAILS constraint 3.

% Option E: oatmeal2=thursday, pb1=tuesday -> NOT same day -> FAILS constraint 3.

% So only Option A satisfies all constraints.

% Verify by encoding as constraints on the candidate
% We'll use a choice to select which option, then verify
{ selected(a..e) } 1.

% If selected A, schedule must match oa_a
schedule(K, B, D) :- selected(a), oa_a(K, B, D).
schedule(K, B, D) :- selected(b), oa_b(K, B, D).
schedule(K, B, D) :- selected(c), oa_c(K, B, D).
schedule(K, B, D) :- selected(d), oa_d(K, B, D).
schedule(K, B, D) :- selected(e), oa_e(K, B, D).

% The constraints above will eliminate invalid options
% Only the selected option that satisfies all constraints will survive

option(X) :- selected(X).

#show option/1.