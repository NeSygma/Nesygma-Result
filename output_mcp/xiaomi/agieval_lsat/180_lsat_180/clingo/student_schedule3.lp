% Students
student(grecia). student(hakeem). student(joe). student(katya). student(louise).

% Days as integers 1-5
day(1). day(2). day(3). day(4). day(5).

% Day names
day_name(1, monday). day_name(2, tuesday). day_name(3, wednesday). day_name(4, thursday). day_name(5, friday).

% Shifts
shift(first). shift(second).

% Each student works exactly two shifts
2 { works(S, D, Sh) : day(D), shift(Sh) } 2 :- student(S).

% Each shift is worked by exactly one student
1 { works(S, D, Sh) : student(S) } 1 :- day(D), shift(Sh).

% No student works both shifts of any day
:- works(S, D, first), works(S, D, second).

% Consecutive days
consecutive(D1, D2) :- day(D1), day(D2), D2 = D1 + 1.

% On two consecutive days, Louise works the second shift
works(louise, D, second) :- consecutive(D1, D), works(louise, D1, second).
works(louise, D1, second) :- consecutive(D1, D), works(louise, D, second).

% Nonconsecutive days (difference > 1)
nonconsecutive(D1, D2) :- day(D1), day(D2), D1 < D2 - 1.
nonconsecutive(D1, D2) :- day(D1), day(D2), D2 < D1 - 1.

% On two nonconsecutive days, Grecia works the first shift
works(grecia, D, first) :- nonconsecutive(D1, D), works(grecia, D1, first).
works(grecia, D1, first) :- nonconsecutive(D1, D), works(grecia, D, first).

% Katya works on Tuesday (day 2) and Friday (day 5)
works(katya, 2, Sh) :- shift(Sh).
works(katya, 5, Sh) :- shift(Sh).

% Hakeem and Joe work on the same day as each other at least once
same_day(D) :- works(hakeem, D, _), works(joe, D, _).
:- not same_day(_).

% Grecia and Louise never work on the same day as each other
:- works(grecia, D, _), works(louise, D, _).

% Show the schedule
#show works/3.