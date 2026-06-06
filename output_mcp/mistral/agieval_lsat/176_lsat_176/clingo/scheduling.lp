% Domains
student(grecia; hakeem; joe; katya; louise).
day(monday; tuesday; wednesday; thursday; friday).
shift(first; second).

% Base facts for consecutive and non-consecutive days
consecutive(monday, tuesday).
consecutive(tuesday, wednesday).
consecutive(wednesday, thursday).
consecutive(thursday, friday).

nonconsecutive(D1, D2) :- day(D1), day(D2), D1 != D2, not consecutive(D1, D2), not consecutive(D2, D1).

% Each student works exactly 2 shifts
2 { works(S, D, SH) : day(D), shift(SH) } 2 :- student(S).

% Each shift is worked by exactly one student
1 { works(S, D, SH) : student(S) } 1 :- day(D), shift(SH).

% No student works both shifts of any day
:- works(S, D, first), works(S, D, second).

% On two consecutive days, Louise works the second shift
% This means there exist two consecutive days where Louise has second shift on both
:- not two_consecutive_louise_second.
two_consecutive_louise_second :- works(louise, D1, second), works(louise, D2, second), consecutive(D1, D2).

% On two non-consecutive days, Grecia works the first shift
% This means there exist two non-consecutive days where Grecia has first shift on both
:- not two_nonconsecutive_grecia_first.
two_nonconsecutive_grecia_first :- works(grecia, D1, first), works(grecia, D2, first), nonconsecutive(D1, D2).

% Katya works on Tuesday and Friday (at least one shift each day)
:- not katya_tuesday.
:- not katya_friday.
katya_tuesday :- works(katya, tuesday, _).
katya_friday :- works(katya, friday, _).

% Hakeem and Joe work on the same day at least once
:- not hakeem_joe_same_day.
hakeem_joe_same_day :- works(hakeem, D, _), works(joe, D, _).

% Grecia and Louise never work on the same day
:- works(grecia, D, _), works(louise, D, _).

% Map the correct answer to option/1 (MANDATORY)
% We need to determine which of A-E MUST be true
% A: Grecia does not work on Tuesday
option(a) :- not works(grecia, tuesday, _).

% B: Hakeem does not work on Wednesday
option(b) :- not works(hakeem, wednesday, _).

% C: Joe does not work on Tuesday
option(c) :- not works(joe, tuesday, _).

% D: Joe does not work on Thursday
option(d) :- not works(joe, thursday, _).

% E: Louise does not work on Tuesday
option(e) :- not works(louise, tuesday, _).

#show option/1.