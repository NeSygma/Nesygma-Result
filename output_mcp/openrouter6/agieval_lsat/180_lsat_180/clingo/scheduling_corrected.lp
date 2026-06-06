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
% She must work at least one shift on each of these days
:- not works(katya, tuesday, first), not works(katya, tuesday, second).
:- not works(katya, friday, first), not works(katya, friday, second).

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

% Show the schedule
#show works/3.

% For multiple-choice: map to option/1
% We'll compute the set of students in fall and spring as a sorted list.
% But we need to compare with answer choices.

% Let's define the answer choices as facts:
% We'll map letters to students: K=katya, L=louise, M=grecia, N=hakeem, O=joe, P=??? (extra)
% Since we have only five students, P is not a student. We'll ignore P.

% For each option, we'll define a condition that checks if the set of students in fall and spring matches.
% We'll use a helper predicate to check membership.

% Option A: fall: K, L, M, O ; spring: N, P
% Since P is not a student, we'll ignore P and require that spring has exactly N (hakeem) and maybe others? But the option says N and P, so only N and P. Since P is not a student, we'll require that spring has only N (hakeem) and no other student? But we have five students, each must work exactly two shifts, so they must appear in either fall or spring. Actually, each student works two shifts, so they could work both shifts in fall, or both in spring, or one in each. So a student could be in both fall and spring sets. The answer choices likely list which students work in fall and which work in spring, possibly with overlap.

% Let's compute for each model the set of students who have at least one shift in fall and at least one shift in spring.
% We'll define:
% student_in_fall(Student) :- works(Student, Day, _), fall_day(Day).
% student_in_spring(Student) :- works(Student, Day, _), spring_day(Day).

% Then we can check which option matches.

% We'll derive the correct option based on the first model (or any model) that satisfies the constraints.
% Since we have multiple models, we need to see which option is consistent with at least one model.

% Let's compute for the first model (we'll use a heuristic: the first model in the output).
% But we cannot see the output before running. We'll run and then add the option mapping in a separate step.
% However, we need to include the option mapping in the same file.

% We'll use a trick: we'll compute the set of students in fall and spring as a string and then compare.
% But that's complex.

% Instead, we'll define a predicate that checks if a given option is satisfied by the current assignment.
% We'll define for each option a condition that the set of students in fall and spring matches the option.

% Since we don't know which option is correct, we'll define all options and then see which one is derived.
% But we need to ensure that exactly one option is derived.

% Let's define the mapping of letters to students:
letter_student(k, katya).
letter_student(l, louise).
letter_student(m, grecia).
letter_student(n, hakeem).
letter_student(o, joe).

% For each option, we'll define a condition that the fall set contains exactly the students listed, and the spring set contains exactly the students listed.
% However, the fall and spring sets may contain extra students (if a student works both fall and spring). We need to consider that.

% We'll define for each option a set of fall letters and spring letters.
% Then we'll check that for each letter in fall, the corresponding student is in fall, and for each letter not in fall, the student is not in fall (unless also in spring? Actually, the option lists which students work in fall and which work in spring. It might be that a student works in both, but the option might list them in one or the other. We'll assume the option lists the students who work at least one shift in that season.

% We'll define:
% option_fall(a, k). option_fall(a, l). option_fall(a, m). option_fall(a, o).
% option_spring(a, n). option_spring(a, p). (p is not a student, so we ignore)

% Then we check that for each letter in option_fall, the student is in student_fall.
% And for each letter in option_spring, the student is in student_spring.
% And also that no other student is in student_fall or student_spring? Not necessarily.

% We'll define a predicate option_satisfied(Option) that checks the above.

% Let's define the options:
option_fall(a, k). option_fall(a, l). option_fall(a, m). option_fall(a, o).
option_spring(a, n). option_spring(a, p). % p is not a student, so we ignore

option_fall(b, k). option_fall(b, l). option_fall(b, n). option_fall(b, o).
option_spring(b, m). option_spring(b, p).

option_fall(c, k). option_fall(c, l). option_fall(c, n). option_fall(c, p).
option_spring(c, m). option_spring(c, o).

option_fall(d, k). option_fall(d, m). option_fall(d, n). option_fall(d, o).
option_spring(d, l). option_spring(d, p).

option_fall(e, m). option_fall(e, o).
option_spring(e, k). option_spring(e, l). option_spring(e, n). option_spring(e, p).

% Now, for each option, we check that all fall letters correspond to students in student_fall, and all spring letters correspond to students in student_spring.
% We also need to ensure that the student sets are exactly as specified? Not necessarily, but we'll assume that the option lists all students that work in that season.

% We'll define a helper: student_in_fall(Student) and student_in_spring(Student) as above.

% For each option, we'll derive option(Option) if:
% For each letter in option_fall(Option, Letter), the corresponding student is in student_fall.
% For each letter in option_spring(Option, Letter), the corresponding student is in student_spring (if the letter corresponds to a student; if letter is p, ignore).

% Additionally, we might need to ensure that no other student is in student_fall or student_spring? Not required by the problem.

% Let's define the conditions:

option(a) :-
    letter_student(k, K), student_fall(K),
    letter_student(l, L), student_fall(L),
    letter_student(m, M), student_fall(M),
    letter_student(o, O), student_fall(O),
    letter_student(n, N), student_spring(N),
    % p is ignored
    true.

option(b) :-
    letter_student(k, K), student_fall(K),
    letter_student(l, L), student_fall(L),
    letter_student(n, N), student_fall(N),
    letter_student(o, O), student_fall(O),
    letter_student(m, M), student_spring(M),
    true.

option(c) :-
    letter_student(k, K), student_fall(K),
    letter_student(l, L), student_fall(L),
    letter_student(n, N), student_fall(N),
    % p is ignored
    letter_student(m, M), student_spring(M),
    letter_student(o, O), student_spring(O),
    true.

option(d) :-
    letter_student(k, K), student_fall(K),
    letter_student(m, M), student_fall(M),
    letter_student(n, N), student_fall(N),
    letter_student(o, O), student_fall(O),
    letter_student(l, L), student_spring(L),
    true.

option(e) :-
    letter_student(m, M), student_fall(M),
    letter_student(o, O), student_fall(O),
    letter_student(k, K), student_spring(K),
    letter_student(l, L), student_spring(L),
    letter_student(n, N), student_spring(N),
    true.

#show option/1.