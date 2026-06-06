% Students and days
student(grecia). student(hakeem). student(joe). student(katya). student(louise).
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).
shift(first). shift(second).

% Time slots: each day has two shifts
time(D, S) :- day(D), shift(S).

% Each shift is worked by exactly one student
1 { works(Student, D, S) : student(Student) } 1 :- time(D, S).

% Each student works exactly two shifts total
2 { works(Student, D, S) : time(D, S) } 2 :- student(Student).

% No student works both shifts of any day
:- works(Student, D, first), works(Student, D, second).

% Louise works exactly two shifts, both are second shifts, and they are on consecutive days
louise_second(D) :- works(louise, D, second).
louise_second_count(N) :- N = #count{D : louise_second(D)}.
:- louise_second_count(N), N != 2.
consecutive_days(monday, tuesday).
consecutive_days(tuesday, wednesday).
consecutive_days(wednesday, thursday).
consecutive_days(thursday, friday).
louise_consecutive :- works(louise, D1, second), works(louise, D2, second), consecutive_days(D1, D2).
:- not louise_consecutive.

% Grecia works exactly two shifts, both are first shifts, and they are on nonconsecutive days
grecia_first(D) :- works(grecia, D, first).
grecia_first_count(N) :- N = #count{D : grecia_first(D)}.
:- grecia_first_count(N), N != 2.
nonconsecutive_days(D1, D2) :- day(D1), day(D2), D1 != D2, 
    not consecutive_days(D1, D2), not consecutive_days(D2, D1).
grecia_nonconsecutive :- works(grecia, D1, first), works(grecia, D2, first), nonconsecutive_days(D1, D2).
:- not grecia_nonconsecutive.

% Katya works on Tuesday and Friday
katya_tuesday :- works(katya, tuesday, _).
katya_friday :- works(katya, friday, _).
:- not katya_tuesday, not katya_friday.

% Additional condition: Katya works the second shift on Tuesday
katya_tuesday_second :- works(katya, tuesday, second).
:- not katya_tuesday_second.

% Hakeem and Joe work on the same day at least once
same_day_hj :- works(hakeem, D, _), works(joe, D, _).
:- not same_day_hj.

% Grecia and Louise never work on the same day
:- works(grecia, D, _), works(louise, D, _).

% Test each option individually
% Option A: Grecia works the first shift on Monday
test_a :- works(grecia, monday, first).
:- not test_a.

#show option_a/0.
#show test_a/0.