% Domains
student(grecia; hakeem; joe; katya; louise).
day(monday; tuesday; wednesday; thursday; friday).
shift(first; second).

% Define consecutive days explicitly
consecutive(monday, tuesday).
consecutive(tuesday, wednesday).
consecutive(wednesday, thursday).
consecutive(thursday, friday).

% Each student works exactly 2 shifts (one per day due to no double shifts)
1 { works(S, D, Sh) : day(D), shift(Sh) } 2 :- student(S).

% Each day/shift is worked by exactly one student
1 { works(S, D, Sh) : student(S) } 1 :- day(D), shift(Sh).

% No student works both shifts of a day
:- works(S, D, first), works(S, D, second).

% Katya works on Tuesday and Friday (exactly one shift each day)
works(katya, tuesday, first) | works(katya, tuesday, second).
works(katya, friday, first) | works(katya, friday, second).

% Hakeem works on Wednesday (exactly one shift)
works(hakeem, wednesday, first) | works(hakeem, wednesday, second).

% Hakeem and Joe work on the same day at least once
same_day_hj :- day(D), works(hakeem, D, _), works(joe, D, _).

% Grecia and Louise never work on the same day
:- day(D), works(grecia, D, _), works(louise, D, _).

% Louise works second shift on exactly two days, and at least one pair must be consecutive
:- #count { D : works(louise, D, second) } != 2.
:- not has_consecutive_louise_second.
has_consecutive_louise_second :- consecutive(D1, D2), works(louise, D1, second), works(louise, D2, second).

% Grecia works first shift on exactly two days, and they must be non-consecutive
:- #count { D : works(grecia, D, first) } != 2.
:- works(grecia, D1, first), works(grecia, D2, first), consecutive(D1, D2).

% Hakeem and Joe must share a day
:- not same_day_hj.

% Define Joe's days
joe_day(D) :- day(D), works(joe, D, _).

% Define the answer options
option(a) :- joe_day(monday), joe_day(wednesday).
option(b) :- joe_day(monday), joe_day(thursday).
option(c) :- joe_day(tuesday), joe_day(wednesday).
option(d) :- joe_day(tuesday), joe_day(thursday).
option(e) :- joe_day(wednesday), joe_day(thursday).

#show option/1.