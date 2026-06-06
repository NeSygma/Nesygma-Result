% Domains
day(1..5).  % Monday=1, Tuesday=2, Wednesday=3, Thursday=4, Friday=5
student(g;h;j;k;l).  % Grecia, Hakeem, Joe, Katya, Louise

% Each day has exactly one first shift worker and one second shift worker
1 { first_shift(S, D) : student(S) } 1 :- day(D).
1 { second_shift(S, D) : student(S) } 1 :- day(D).

% Derive which days each student works
works(S, D) :- first_shift(S, D).
works(S, D) :- second_shift(S, D).

% No student works both shifts on a day
:- first_shift(S, D), second_shift(S, D).

% Each student works exactly two days
:- student(S), #count { D : works(S, D) } != 2.

% Katya works on Tuesday (2) and Friday (5)
works(k, 2).
works(k, 5).

% Louise works second shift on two consecutive days (at least one such pair)
some_consecutive_louise :- second_shift(l, D), second_shift(l, D+1), day(D), day(D+1).
:- not some_consecutive_louise.

% Grecia works first shift on two nonconsecutive days (at least one such pair)
some_nonconsecutive_grecia :- first_shift(g, D1), first_shift(g, D2), D1 < D2, D2 > D1+1, day(D1), day(D2).
:- not some_nonconsecutive_grecia.

% Hakeem and Joe work on the same day at least once
same_day_hj :- works(h, D), works(j, D), day(D).
:- not same_day_hj.

% Grecia and Louise never work on the same day
:- works(g, D), works(l, D), day(D).

% Hypothetical: Hakeem works on Wednesday (3)
works(h, 3).

% Show results
#show first_shift/2.
#show second_shift/2.
#show works/2.