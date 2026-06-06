% Students
student(grecia). student(hakeem). student(joe). student(katya). student(louise).

% Days
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).

% Shifts
shift(first). shift(second).

% Time ordering for consecutive days
consecutive(monday, tuesday).
consecutive(tuesday, wednesday).
consecutive(wednesday, thursday).
consecutive(thursday, friday).

% Each student works exactly two shifts
1 { works(Student, Day, Shift) : day(Day), shift(Shift) } 2 :- student(Student).

% Each shift is worked by exactly one student
1 { works(Student, Day, Shift) : student(Student) } 1 :- day(Day), shift(Shift).

% No student works both shifts of any day
:- works(Student, Day, first), works(Student, Day, second).

% On two consecutive days, Louise works the second shift
% This means there exists at least one pair of consecutive days where Louise works second shift on both
louise_consecutive :- works(louise, D1, second), works(louise, D2, second), consecutive(D1, D2).
% Actually, the constraint says "On two consecutive days, Louise works the second shift"
% This means there is at least one pair of consecutive days where she works second shift on both
% Let's make it more precise: there must exist D1, D2 consecutive such that Louise works second on both
:- not louise_consecutive.

% On two nonconsecutive days, Grecia works the first shift
% Nonconsecutive means not consecutive (and not the same day)
nonconsecutive(D1, D2) :- day(D1), day(D2), D1 != D2, not consecutive(D1, D2), not consecutive(D2, D1).
grecia_nonconsecutive :- works(grecia, D1, first), works(grecia, D2, first), nonconsecutive(D1, D2).
:- not grecia_nonconsecutive.

% Katya works on Tuesday and Friday
% This means Katya works at least one shift on Tuesday and at least one shift on Friday
katya_tuesday :- works(katya, tuesday, _).
katya_friday :- works(katya, friday, _).
:- not katya_tuesday, not katya_friday.

% Hakeem and Joe work on the same day as each other at least once
same_day_hakeem_joe :- works(hakeem, D, _), works(joe, D, _).
:- not same_day_hakeem_joe.

% Grecia and Louise never work on the same day as each other
:- works(grecia, D, _), works(louise, D, _).

% Helper: Student works on a day (any shift)
works_on_day(Student, Day) :- works(Student, Day, _).

% Evaluate the answer choices
% (A) Grecia does not work at the gallery on Tuesday.
option(a) :- not works_on_day(grecia, tuesday).

% (B) Hakeem does not work at the gallery on Wednesday.
option(b) :- not works_on_day(hakeem, wednesday).

% (C) Joe does not work at the gallery on Tuesday.
option(c) :- not works_on_day(joe, tuesday).

% (D) Joe does not work at the gallery on Thursday.
option(d) :- not works_on_day(joe, thursday).

% (E) Louise does not work at the gallery on Tuesday.
option(e) :- not works_on_day(louise, tuesday).

#show option/1.