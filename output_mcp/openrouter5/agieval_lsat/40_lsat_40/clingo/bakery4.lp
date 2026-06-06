%% Let's get more models with full assignments visible
day(mon; tue; wed; thu; fri).
kind(oatmeal; peanut_butter; sugar).
batch(1..3).

{ assigned(Kind, Batch, Day) : day(Day) } 1 :- kind(Kind), batch(Batch).

:- assigned(K, B1, D), assigned(K, B2, D), B1 != B2.
:- not assigned(_, _, mon).
:- assigned(oatmeal, 2, D1), assigned(peanut_butter, 1, D2), D1 != D2.
assigned(sugar, 2, thu).
:- assigned(_, _, wed).

%% Let's see full assignments
#show assigned/3.