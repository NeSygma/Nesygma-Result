% Domains
student(grecia). student(hakeem). student(joe). student(katya). student(louise).
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).
shift(first). shift(second).

% Days in order for consecutive check
day_order(monday, tuesday).
day_order(tuesday, wednesday).
day_order(wednesday, thursday).
day_order(thursday, friday).

% Non-consecutive days (with at least one day in between)
nonconsecutive(monday, wednesday).
nonconsecutive(monday, thursday).
nonconsecutive(monday, friday).
nonconsecutive(tuesday, thursday).
nonconsecutive(tuesday, friday).
nonconsecutive(wednesday, friday).

% Base schedule: each day has two shifts, each shift has exactly one student
1 { works(Student, Day, Shift) : student(Student) } 1 :- day(Day), shift(Shift).

% Each student works exactly two shifts
:- student(Student), #count { Day, Shift : works(Student, Day, Shift) } != 2.

% No student works both shifts of any day
:- student(Student), day(Day), works(Student, Day, first), works(Student, Day, second).

% On two consecutive days, Louise works the second shift
:- day_order(Day1, Day2), not works(louise, Day1, second), not works(louise, Day2, second).

% On two nonconsecutive days, Grecia works the first shift
:- nonconsecutive(Day1, Day2), not works(grecia, Day1, first), not works(grecia, Day2, first).

% Katya works on Tuesday and Friday (at least one shift each day)
:- day(tuesday), not works(katya, tuesday, first), not works(katya, tuesday, second).
:- day(friday), not works(katya, friday, first), not works(katya, friday, second).

% Hakeem and Joe work on the same day as each other at least once
:- not same_day(hakeem, joe).
same_day(S1, S2) :- day(Day), works(S1, Day, _), works(S2, Day, _), S1 != S2.

% Grecia and Louise never work on the same day as each other
:- day(Day), works(grecia, Day, _), works(louise, Day, _).

% Define the second shift schedules for each choice
second_shift_a(monday, hakeem).
second_shift_a(tuesday, louise).
second_shift_a(wednesday, louise).
second_shift_a(thursday, hakeem).
second_shift_a(friday, katya).

second_shift_b(monday, joe).
second_shift_b(tuesday, hakeem).
second_shift_b(wednesday, grecia).
second_shift_b(thursday, louise).
second_shift_b(friday, louise).

second_shift_c(monday, joe).
second_shift_c(tuesday, katya).
second_shift_c(wednesday, hakeem).
second_shift_c(thursday, louise).
second_shift_c(friday, katya).

second_shift_d(monday, louise).
second_shift_d(tuesday, katya).
second_shift_d(wednesday, joe).
second_shift_d(thursday, louise).
second_shift_d(friday, katya).

second_shift_e(monday, louise).
second_shift_e(tuesday, louise).
second_shift_e(wednesday, hakeem).
second_shift_e(thursday, joe).
second_shift_e(friday, joe).

% Check if the second shifts match a given choice
matches_choice(a) :-
    day(Day),
    works(Student, Day, second),
    second_shift_a(Day, Student).

matches_choice(b) :-
    day(Day),
    works(Student, Day, second),
    second_shift_b(Day, Student).

matches_choice(c) :-
    day(Day),
    works(Student, Day, second),
    second_shift_c(Day, Student).

matches_choice(d) :-
    day(Day),
    works(Student, Day, second),
    second_shift_d(Day, Student).

matches_choice(e) :-
    day(Day),
    works(Student, Day, second),
    second_shift_e(Day, Student).

% Ensure all second shifts match the choice
:- matches_choice(C), day(Day), works(Student, Day, second), not second_shift(C, Day, Student).
:- matches_choice(C), day(Day), second_shift(C, Day, Student), not works(Student, Day, second).

second_shift(a, Day, Student) :- second_shift_a(Day, Student).
second_shift(b, Day, Student) :- second_shift_b(Day, Student).
second_shift(c, Day, Student) :- second_shift_c(Day, Student).
second_shift(d, Day, Student) :- second_shift_d(Day, Student).
second_shift(e, Day, Student) :- second_shift_e(Day, Student).

% Map the correct answer to option/1
option(a) :- matches_choice(a).
option(b) :- matches_choice(b).
option(c) :- matches_choice(c).
option(d) :- matches_choice(d).
option(e) :- matches_choice(e).

#show option/1.