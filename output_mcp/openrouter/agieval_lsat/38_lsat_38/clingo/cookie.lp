% Days 1..5 represent Monday..Friday
day(1..5).
% Types of cookies
type(oatmeal; peanut; sugar).
% Batch indices 1..3
idx(1..3).
% Define each batch as a fact
batch(T,I) :- type(T), idx(I).

% Assign each batch to exactly one day
1 { assign(T,I,D) : day(D) } 1 :- batch(T,I).

% No two batches of same type on same day
:- assign(T,I,D), assign(T,J,D), I != J.

% O2 same day as P1 (second oatmeal with first peanut)
:- assign(oatmeal,2,D), not assign(peanut,1,D).
:- assign(peanut,1,D), not assign(oatmeal,2,D).

% Second sugar batch on Thursday (day 4)
:- assign(sugar,2,D), D != 4.
% Force it to be on day 4
assign(sugar,2,4) :- day(4).

% Ordering constraints: first < second < third for each type
% Oatmeal ordering
:- assign(oatmeal,1,D1), assign(oatmeal,2,D2), D1 >= D2.
:- assign(oatmeal,2,D2), assign(oatmeal,3,D3), D2 >= D3.
% Peanut ordering
:- assign(peanut,1,D1), assign(peanut,2,D2), D1 >= D2.
:- assign(peanut,2,D2), assign(peanut,3,D3), D2 >= D3.
% Sugar ordering
:- assign(sugar,1,D1), assign(sugar,2,D2), D1 >= D2.
:- assign(sugar,2,D2), assign(sugar,3,D3), D2 >= D3.

% At least one batch on Monday (day 1)
:- not assigned_any(1).
assigned_any(D) :- assign(_,_,D).

% Count batches per day
cnt(D,N) :- N = #count { T,I : assign(T,I,D) }.

% Maximize number of days that have three batches
#maximize { 1,D : cnt(D,3) }.

% Days without three batches in the optimal model
day_without_three(D) :- day(D), not cnt(D,3).
N = #count { D : day_without_three(D) }.

option(a) :- N = 1.
option(b) :- N = 2.
option(c) :- N = 3.
option(d) :- N = 4.
option(e) :- N = 5.

#show option/1.