% Scheduling Problem for Art Gallery with Options

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

% On two consecutive days, Louise works the second shift
consecutive_day(D1, D2) :- day(D1), day(D2), D1 = monday, D2 = tuesday.
consecutive_day(D1, D2) :- day(D1), day(D2), D1 = tuesday, D2 = wednesday.
consecutive_day(D1, D2) :- day(D1), day(D2), D1 = wednesday, D2 = thursday.
consecutive_day(D1, D2) :- day(D1), day(D2), D1 = thursday, D2 = friday.

louise_second_on_consecutive :- works(louise, D1, second), works(louise, D2, second), consecutive_day(D1, D2).
:- not louise_second_on_consecutive.

% On two nonconsecutive days, Grecia works the first shift
nonconsecutive_day(D1, D2) :- day(D1), day(D2), D1 != D2, not consecutive_day(D1, D2), not consecutive_day(D2, D1).
grecia_first_on_nonconsecutive :- works(grecia, D1, first), works(grecia, D2, first), nonconsecutive_day(D1, D2).
:- not grecia_first_on_nonconsecutive.

% Katya works on Tuesday and Friday
:- not works(katya, tuesday, first), not works(katya, tuesday, second).
:- not works(katya, friday, first), not works(katya, friday, second).

% Hakeem and Joe work on the same day as each other at least once
same_day_hakeem_joe :- works(hakeem, Day, _), works(joe, Day, _).
:- not same_day_hakeem_joe.

% Grecia and Louise never work on the same day as each other
:- works(grecia, Day, _), works(louise, Day, _).

% Define fall and spring days (arbitrary: Monday-Wednesday fall, Thursday-Friday spring)
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

% Option choice
1 { option_choice(a); option_choice(b); option_choice(c); option_choice(d); option_choice(e) } 1.

% For each option, define the required fall and spring sets (excluding P)
% Option A: fall: k, l, m, o ; spring: n
option_fall(a, k). option_fall(a, l). option_fall(a, m). option_fall(a, o).
option_spring(a, n).

% Option B: fall: k, l, n, o ; spring: m
option_fall(b, k). option_fall(b, l). option_fall(b, n). option_fall(b, o).
option_spring(b, m).

% Option C: fall: k, l, n ; spring: m, o
option_fall(c, k). option_fall(c, l). option_fall(c, n).
option_spring(c, m). option_spring(c, o).

% Option D: fall: k, m, n, o ; spring: l
option_fall(d, k). option_fall(d, m). option_fall(d, n). option_fall(d, o).
option_spring(d, l).

% Option E: fall: m, o ; spring: k, l, n
option_fall(e, m). option_fall(e, o).
option_spring(e, k). option_spring(e, l). option_spring(e, n).

% Constraints for each option
% If option_choice(A) is true, then:
% 1. For each letter in option_fall(A, Letter), the corresponding student must be in student_fall.
% 2. For each student not in option_fall(A, Letter), they must not be in student_fall.
% 3. Similarly for spring.

% Helper: student_in_fall(Student) and student_in_spring(Student) are already defined.

% For option A:
:- option_choice(a), letter_student(L, S), option_fall(a, L), not student_fall(S).
:- option_choice(a), letter_student(L, S), not option_fall(a, L), student_fall(S).
:- option_choice(a), letter_student(L, S), option_spring(a, L), not student_spring(S).
:- option_choice(a), letter_student(L, S), not option_spring(a, L), student_spring(S).

% For option B:
:- option_choice(b), letter_student(L, S), option_fall(b, L), not student_fall(S).
:- option_choice(b), letter_student(L, S), not option_fall(b, L), student_fall(S).
:- option_choice(b), letter_student(L, S), option_spring(b, L), not student_spring(S).
:- option_choice(b), letter_student(L, S), not option_spring(b, L), student_spring(S).

% For option C:
:- option_choice(c), letter_student(L, S), option_fall(c, L), not student_fall(S).
:- option_choice(c), letter_student(L, S), not option_fall(c, L), student_fall(S).
:- option_choice(c), letter_student(L, S), option_spring(c, L), not student_spring(S).
:- option_choice(c), letter_student(L, S), not option_spring(c, L), student_spring(S).

% For option D:
:- option_choice(d), letter_student(L, S), option_fall(d, L), not student_fall(S).
:- option_choice(d), letter_student(L, S), not option_fall(d, L), student_fall(S).
:- option_choice(d), letter_student(L, S), option_spring(d, L), not student_spring(S).
:- option_choice(d), letter_student(L, S), not option_spring(d, L), student_spring(S).

% For option E:
:- option_choice(e), letter_student(L, S), option_fall(e, L), not student_fall(S).
:- option_choice(e), letter_student(L, S), not option_fall(e, L), student_fall(S).
:- option_choice(e), letter_student(L, S), option_spring(e, L), not student_spring(S).
:- option_choice(e), letter_student(L, S), not option_spring(e, L), student_spring(S).

% Derive the option that is chosen
option(A) :- option_choice(A).

#show option/1.