% Domain: Students and Days
student(grecia; hakeem; joe; katya; louise).
day(monday; tuesday; wednesday; thursday; friday).
shift(first; second).

% Order of days for consecutive/nonconsecutive checks
day_order(monday, 1).
day_order(tuesday, 2).
day_order(wednesday, 3).
day_order(thursday, 4).
day_order(friday, 5).

% Each student works exactly two shifts
1 { works(Student, Day, Shift) : day(Day), shift(Shift) } 2 :- student(Student).

% Each shift is worked by exactly one student
:- day(Day), shift(Shift), not 1 { works(Student, Day, Shift) : student(Student) } 1.

% No student works both shifts of any day
:- student(Student), day(Day), shift(Shift1), shift(Shift2), Shift1 != Shift2, works(Student, Day, Shift1), works(Student, Day, Shift2).

% There exist two consecutive days where Louise works the second shift
consecutive_day(D1, D2) :- day_order(D1, O1), day_order(D2, O2), O2 = O1 + 1.
:- not 1 { works(louise, D2, second) : consecutive_day(_, D2) } 1.

% There exist two nonconsecutive days where Grecia works the first shift
nonconsecutive_day(D1, D2) :- day_order(D1, O1), day_order(D2, O2), O1 < O2, O2 - O1 > 1.
:- not 1 { works(grecia, D1, first) : nonconsecutive_day(D1, _) } 1.
:- not 1 { works(grecia, D2, first) : nonconsecutive_day(_, D2) } 1.

% Katya works on Tuesday and Friday
:- not works(katya, tuesday, _).
:- not works(katya, friday, _).

% Hakeem and Joe work on the same day as each other at least once
same_day_work :- day(Day), works(hakeem, Day, _), works(joe, Day, _).
:- not same_day_work.

% Grecia and Louise never work on the same day as each other
:- day(Day), works(grecia, Day, _), works(louise, Day, _).

% --- Answer Mapping ---
% (A) Grecia does not work at the gallery on Tuesday.
option(a) :- not works(grecia, tuesday, _).

% (B) Hakeem does not work at the gallery on Wednesday.
option(b) :- not works(hakeem, wednesday, _).

% (C) Joe does not work at the gallery on Tuesday.
option(c) :- not works(joe, tuesday, _).

% (D) Joe does not work at the gallery on Thursday.
option(d) :- not works(joe, thursday, _).

% (E) Louise does not work at the gallery on Tuesday.
option(e) :- not works(louise, tuesday, _).

#show option/1.