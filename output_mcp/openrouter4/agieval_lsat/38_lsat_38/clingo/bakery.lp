day(1..5).  % 1=Mon,2=Tue,3=Wed,4=Thu,5=Fri
kind(oatmeal; peanut; sugar).
order(1;2;3).

batch(K,O) :- kind(K), order(O).

% assign each batch to a day
{ assign(K,O,D) : day(D) } 1 :- batch(K,O).

% no two same kind on same day
:- kind(K), day(D), #count{O : assign(K,O,D)} > 1.

% at least one batch on Monday
:- #count{K,O : assign(K,O,1)} = 0.

% O2 and P1 same day
:- assign(oatmeal,2,D1), assign(peanut,1,D2), D1 != D2.

% S2 on Thursday (day 4)
assign(sugar,2,4).

% count batches per day
batches_on_day(D, N) :- day(D), N = #count{K,O : assign(K,O,D)}.

% show
#show assign/3.
#show batches_on_day/2.