% Scheduling Problem for Art Gallery

% Days: Monday to Friday
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).

% Shifts: first and second
shift(first). shift(second).

% Students
student(grecia). student(hakeem). student(joe). student(katya). student(louise).

% Each student works exactly two shifts
2 { works(Student, Day, Shift) : day(Day), shift(Shift) } 2 :- student(Student).

% Each shift is worked by exactly one student
1 { works(Student, Day, Shift) : student(Student) } 1 :- day(Day), shift(Shift).

% No student works both shifts of any day
:- works(Student, Day, first), works(Student, Day, second).

% Consecutive days definition
consecutive(monday, tuesday).
consecutive(tuesday, wednesday).
consecutive(wednesday, thursday).
consecutive(thursday, friday).

% On two consecutive days, Louise works the second shift
louise_consecutive_second :- works(louise, D1, second), works(louise, D2, second), consecutive(D1, D2).
:- not louise_consecutive_second.

% Nonconsecutive days definition (days that are not consecutive)
nonconsecutive(D1, D2) :- day(D1), day(D2), D1 != D2, not consecutive(D1, D2), not consecutive(D2, D1).

% On two nonconsecutive days, Grecia works the first shift
grecia_nonconsecutive_first :- works(grecia, D1, first), works(grecia, D2, first), nonconsecutive(D1, D2).
:- not grecia_nonconsecutive_first.

% Katya works on Tuesday and Friday (any shift)
katya_tuesday :- works(katya, tuesday, _).
katya_friday :- works(katya, friday, _).
:- not katya_tuesday.
:- not katya_friday.

% Hakeem and Joe work on the same day as each other at least once
same_day_hakeem_joe :- works(hakeem, Day, _), works(joe, Day, _).
:- not same_day_hakeem_joe.

% Grecia and Louise never work on the same day as each other
:- works(grecia, Day, _), works(louise, Day, _).

% Define fall and spring days
fall_day(monday). fall_day(tuesday). fall_day(wednesday).
spring_day(thursday). spring_day(friday).

% Students who work on fall days
student_fall(Student) :- works(Student, Day, _), fall_day(Day).
% Students who work on spring days
student_spring(Student) :- works(Student, Day, _), spring_day(Day).

% Map letters to students
letter_student(k, katya).
letter_student(l, louise).
letter_student(m, grecia).
letter_student(n, hakeem).
letter_student(o, joe).

% Option definitions
option_fall(a, k). option_fall(a, l). option_fall(a, m). option_fall(a, o).
option_spring(a, n). option_spring(a, p).

option_fall(b, k). option_fall(b, l). option_fall(b, n). option_fall(b, o).
option_spring(b, m). option_spring(b, p).

option_fall(c, k). option_fall(c, l). option_fall(c, n). option_fall(c, p).
option_spring(c, m). option_spring(c, o).

option_fall(d, k). option_fall(d, m). option_fall(d, n). option_fall(d, o).
option_spring(d, l). option_spring(d, p).

option_fall(e, m). option_fall(e, o).
option_spring(e, k). option_spring(e, l). option_spring(e, n). option_spring(e, p).

% Check each option
option(a) :- 
    letter_student(L, S), option_fall(a, L), student_fall(S),
    letter_student(L2, S2), option_spring(a, L2), student_spring(S2),
    not (letter_student(L3, S3), option_fall(a, L3), not student_fall(S3)),
    not (letter_student(L4, S4), option_spring(a, L4), not student_spring(S4)).

option(b) :- 
    letter_student(L, S), option_fall(b, L), student_fall(S),
    letter_student(L2, S2), option_spring(b, L2), student_spring(S2),
    not (letter_student(L3, S3), option_fall(b, L3), not student_fall(S3)),
    not (letter_student(L4, S4), option_spring(b, L4), not student_spring(S4)).

option(c) :- 
    letter_student(L, S), option_fall(c, L), student_fall(S),
    letter_student(L2, S2), option_spring(c, L2), student_spring(S2),
    not (letter_student(L3, S3), option_fall(c, L3), not student_fall(S3)),
    not (letter_student(L4, S4), option_spring(c, L4), not student_spring(S4)).

option(d) :- 
    letter_student(L, S), option_fall(d, L), student_fall(S),
    letter_student(L2, S2), option_spring(d, L2), student_spring(S2),
    not (letter_student(L3, S3), option_fall(d, L3), not student_fall(S3)),
    not (letter_student(L4, S4), option_spring(d, L4), not student_spring(S4)).

option(e) :- 
    letter_student(L, S), option_fall(e, L), student_fall(S),
    letter_student(L2, S2), option_spring(e, L2), student_spring(S2),
    not (letter_student(L3, S3), option_fall(e, L3), not student_fall(S3)),
    not (letter_student(L4, S4), option_spring(e, L4), not student_spring(S4)).

#show option/1.