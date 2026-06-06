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

% Check if each option holds in all models
% We'll use a different approach: check if any model violates each option

% Option A: Exactly three batches on Tuesday
violate_a :- batches_on_day(tue, N), N != 3.

% Option B: Exactly three batches on Friday  
violate_b :- batches_on_day(fri, N), N != 3.

% Option C: At least two batches on Monday
violate_c :- batches_on_day(mon, N), N < 2.

% Option D: At least two batches on Thursday
violate_d :- batches_on_day(thu, N), N < 2.

% Option E: Fewer batches on Monday than Tuesday
violate_e :- batches_on_day(mon, M), batches_on_day(tue, T), M >= T.

% Show which options are violated
#show violate_a/0.
#show violate_b/0.
#show violate_c/0.
#show violate_d/0.
#show violate_e/0.
#show assign/3.
#show batches_on_day/2.