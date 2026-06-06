% Domains
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).
kind(oatmeal). kind(pb). kind(sugar).
batch(1). batch(2). batch(3).

% Define option choices
option_name(a). option_name(b). option_name(c). option_name(d). option_name(e).

% Choice: select exactly one option
1 { selected(X) : option_name(X) } 1.

% Option A: oatmeal: Mon, Wed, Thu; pb: Wed, Thu, Fri; sugar: Mon, Thu, Fri
oa(oatmeal, 1, monday, a). oa(oatmeal, 2, wednesday, a). oa(oatmeal, 3, thursday, a).
oa(pb, 1, wednesday, a). oa(pb, 2, thursday, a). oa(pb, 3, friday, a).
oa(sugar, 1, monday, a). oa(sugar, 2, thursday, a). oa(sugar, 3, friday, a).

% Option B: oatmeal: Mon, Tue, Thu; pb: Tue, Wed, Thu; sugar: Mon, Wed, Thu
oa(oatmeal, 1, monday, b). oa(oatmeal, 2, tuesday, b). oa(oatmeal, 3, thursday, b).
oa(pb, 1, tuesday, b). oa(pb, 2, wednesday, b). oa(pb, 3, thursday, b).
oa(sugar, 1, monday, b). oa(sugar, 2, wednesday, b). oa(sugar, 3, thursday, b).

% Option C: oatmeal: Tue, Wed, Thu; pb: Wed, Thu, Fri; sugar: Tue, Thu, Fri
oa(oatmeal, 1, tuesday, c). oa(oatmeal, 2, wednesday, c). oa(oatmeal, 3, thursday, c).
oa(pb, 1, wednesday, c). oa(pb, 2, thursday, c). oa(pb, 3, friday, c).
oa(sugar, 1, tuesday, c). oa(sugar, 2, thursday, c). oa(sugar, 3, friday, c).

% Option D: oatmeal: Mon, Tue, Thu; pb: Mon, Wed, Thu; sugar: Mon, Thu, Fri
oa(oatmeal, 1, monday, d). oa(oatmeal, 2, tuesday, d). oa(oatmeal, 3, thursday, d).
oa(pb, 1, monday, d). oa(pb, 2, wednesday, d). oa(pb, 3, thursday, d).
oa(sugar, 1, monday, d). oa(sugar, 2, thursday, d). oa(sugar, 3, friday, d).

% Option E: oatmeal: Mon, Thu, Fri; pb: Tue, Wed, Thu; sugar: Mon, Thu, Fri
oa(oatmeal, 1, monday, e). oa(oatmeal, 2, thursday, e). oa(oatmeal, 3, friday, e).
oa(pb, 1, tuesday, e). oa(pb, 2, wednesday, e). oa(pb, 3, thursday, e).
oa(sugar, 1, monday, e). oa(sugar, 2, thursday, e). oa(sugar, 3, friday, e).

% Constraint 1: No two batches of the same kind on the same day
:- selected(O), oa(K, B1, D, O), oa(K, B2, D, O), B1 != B2.

% Constraint 2: At least one batch on Monday
:- selected(O), not made_on_monday(O).
made_on_monday(O) :- oa(_, _, monday, O).

% Constraint 3: Second batch of oatmeal same day as first batch of peanut butter
:- selected(O), oa(oatmeal, 2, D1, O), oa(pb, 1, D2, O), D1 != D2.

% Constraint 4: Second batch of sugar is Thursday
:- selected(O), oa(sugar, 2, D, O), D != thursday.

option(X) :- selected(X).

#show option/1.