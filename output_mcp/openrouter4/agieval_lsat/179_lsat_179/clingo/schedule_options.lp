% Domains
student(grecia; hakeem; joe; katya; louise).
day(mon; tue; wed; thu; fri).
shift(first; second).

% Consecutive day pairs
consecutive(mon, tue).
consecutive(tue, wed).
consecutive(wed, thu).
consecutive(thu, fri).

% Non-consecutive day pairs
nonconsecutive(D1, D2) :- day(D1), day(D2), D1 < D2, not consecutive(D1, D2).

% Option IDs
option_id(a; b; c; d; e).

% Choose exactly one option to test
1 { test_option(O) : option_id(O) } 1.

% Each shift is assigned exactly one student
1 { works(S, D, Sh) : student(S) } 1 :- day(D), shift(Sh).

% Each student works exactly 2 shifts
2 { works(S, D, Sh) : day(D), shift(Sh) } 2 :- student(S).

% No student works both shifts of any day
:- student(S), day(D), works(S, D, first), works(S, D, second).

% On two consecutive days, Louise works the second shift
:- #count { D1,D2 : consecutive(D1,D2), works(louise, D1, second), works(louise, D2, second) } = 0.

% On two nonconsecutive days, Grecia works the first shift
:- #count { D1,D2 : nonconsecutive(D1,D2), works(grecia, D1, first), works(grecia, D2, first) } = 0.

% Katya works on Tuesday and Friday (at least one shift each)
:- { works(katya, tue, first); works(katya, tue, second) } 0.
:- { works(katya, fri, first); works(katya, fri, second) } 0.

% Hakeem and Joe work on the same day as each other at least once
same_day(D) :- works(hakeem, D, Sh1), works(joe, D, Sh2).
:- { same_day(D) : day(D) } 0.

% Grecia and Louise never work on the same day as each other
:- day(D), works(grecia, D, _), works(louise, D, _).

% Given condition: Katya works the second shift on Tuesday
works(katya, tue, second).

% Option-specific constraints
% (A) Grecia works the first shift on Monday
works(grecia, mon, first) :- test_option(a).

% (B) Hakeem works the first shift on Monday
works(hakeem, mon, first) :- test_option(b).

% (C) Hakeem works the second shift on Wednesday
works(hakeem, wed, second) :- test_option(c).

% (D) Joe works the second shift on Thursday
works(joe, thu, second) :- test_option(d).

% (E) Louise works the second shift on Monday
works(louise, mon, second) :- test_option(e).

#show test_option/1.