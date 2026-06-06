% Students
student(grecia). student(hakeem). student(joe). student(katya). student(louise).

% Days
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).

% Shifts
shift(first). shift(second).

% Each student works exactly two shifts
2 { works(S, D, Sh) : day(D), shift(Sh) } 2 :- student(S).

% Each shift is worked by exactly one student
1 { works(S, D, Sh) : student(S) } 1 :- day(D), shift(Sh).

% No student works both shifts of any day
:- works(S, D, first), works(S, D, second).

% On two consecutive days, Louise works the second shift
consecutive(D1, D2) :- day(D1), day(D2), D2 = D1 + 1.
works(louise, D, second) :- consecutive(D1, D), works(louise, D1, second).
works(louise, D1, second) :- consecutive(D1, D), works(louise, D, second).

% On two nonconsecutive days, Grecia works the first shift
nonconsecutive(D1, D2) :- day(D1), day(D2), |D1 - D2| > 1.
works(grecia, D, first) :- nonconsecutive(D1, D), works(grecia, D1, first).
works(grecia, D1, first) :- nonconsecutive(D1, D), works(grecia, D, first).

% Katya works on Tuesday and Friday
works(katya, tuesday, Sh) :- shift(Sh).
works(katya, friday, Sh) :- shift(Sh).

% Hakeem and Joe work on the same day as each other at least once
same_day(D) :- works(hakeem, D, _), works(joe, D, _).
:- not same_day(_).

% Grecia and Louise never work on the same day as each other
:- works(grecia, D, _), works(louise, D, _).

% Show the schedule
#show works/3.