% Days
day(1..5).
% Shifts
shift(1..2).
% Students
student(grecia). student(hakeem). student(joe). student(katya). student(louise).

% Assignment: works(Student, Day, Shift)
1 { works(Student, Day, Shift) : student(Student) } 1 :- day(Day), shift(Shift).

% Each student works exactly two shifts
2 { works(Student, Day, Shift) : day(Day), shift(Shift) } 2 :- student(Student).

% No student works both shifts on same day
:- works(Student, Day, 1), works(Student, Day, 2).

% Louise works second shift on two consecutive days
consecutive(D, D+1) :- day(D), day(D+1).
has_consecutive_louise :- works(louise, D, 2), works(louise, D+1, 2), consecutive(D, D+1).
:- not has_consecutive_louise.

% Grecia works first shift on two nonconsecutive days
nonconsecutive(D1, D2) :- day(D1), day(D2), D1 < D2, D2 >= D1+2.
has_nonconsecutive_grecia :- works(grecia, D1, 1), works(grecia, D2, 1), nonconsecutive(D1, D2).
:- not has_nonconsecutive_grecia.

% Katya works on Tuesday and Friday
1 { works(katya, 2, S) : shift(S) } 1.
1 { works(katya, 5, S) : shift(S) } 1.

% Hakeem and Joe work on the same day at least once
same_day_hj :- works(hakeem, D, _), works(joe, D, _).
:- not same_day_hj.

% Grecia and Louise never work on the same day
:- works(grecia, D, _), works(louise, D, _).

% Options
condition_a :- not works(grecia, 2, _).
condition_b :- not works(hakeem, 3, _).
condition_c :- not works(joe, 2, _).
condition_d :- not works(joe, 4, _).
condition_e :- not works(louise, 2, _).

option(a) :- condition_a.
option(b) :- condition_b.
option(c) :- condition_c.
option(d) :- condition_d.
option(e) :- condition_e.

#show option/1.
#show works/3.