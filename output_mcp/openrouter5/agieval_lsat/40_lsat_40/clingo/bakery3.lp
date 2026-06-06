%% Let's get more models to see patterns
%% Problem: Bakery cookies scheduling
day(mon; tue; wed; thu; fri).
kind(oatmeal; peanut_butter; sugar).
batch(1..3).

{ assigned(Kind, Batch, Day) : day(Day) } 1 :- kind(Kind), batch(Batch).

:- assigned(K, B1, D), assigned(K, B2, D), B1 != B2.
:- not assigned(_, _, mon).
:- assigned(oatmeal, 2, D1), assigned(peanut_butter, 1, D2), D1 != D2.
assigned(sugar, 2, thu).
:- assigned(_, _, wed).

%% Get all models - let's count more
mon_count(N) :- N = #count{K,B : assigned(K,B,mon)}.
tue_count(N) :- N = #count{K,B : assigned(K,B,tue)}.
thu_count(N) :- N = #count{K,B : assigned(K,B,thu)}.
fri_count(N) :- N = #count{K,B : assigned(K,B,fri)}.

#show mon_count/1.
#show tue_count/1.
#show thu_count/1.
#show fri_count/1.