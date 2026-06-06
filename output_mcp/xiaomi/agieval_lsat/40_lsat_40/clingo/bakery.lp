% Domains
cookie(oatmeal). cookie(peanut_butter). cookie(sugar).
batch(1). batch(2). batch(3).
day(mon). day(tue). day(wed). day(thu). day(fri).

% Each batch of each cookie type is assigned to exactly one day
1 { assign(C, B, D) : day(D) } 1 :- cookie(C), batch(B).

% No two batches of the same cookie type on the same day
:- assign(C, B1, D), assign(C, B2, D), B1 != B2.

% At least one batch on Monday
:- not assign(_, _, mon).

% Second oatmeal batch same day as first peanut butter batch
assign(oatmeal, 2, D) :- assign(peanut_butter, 1, D).
assign(peanut_butter, 1, D) :- assign(oatmeal, 2, D).

% Second sugar batch on Thursday
assign(sugar, 2, thu).

% No batches on Wednesday (given condition)
:- assign(_, _, wed).

% Count batches per day
batches_on_day(D, N) :- day(D), N = #count{C,B : assign(C,B,D)}.

% Evaluate each option
% (A) Exactly three batches on Tuesday
option(a) :- batches_on_day(tue, 3).

% (B) Exactly three batches on Friday
option(b) :- batches_on_day(fri, 3).

% (C) At least two batches on Monday
option(c) :- batches_on_day(mon, N), N >= 2.

% (D) At least two batches on Thursday
option(d) :- batches_on_day(thu, N), N >= 2.

% (E) Fewer batches on Monday than Tuesday
option(e) :- batches_on_day(mon, M), batches_on_day(tue, T), M < T.

#show option/1.
#show assign/3.
#show batches_on_day/2.