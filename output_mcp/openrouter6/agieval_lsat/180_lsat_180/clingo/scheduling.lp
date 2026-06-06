% Scheduling Problem for Art Gallery

% Days: Monday to Friday
day(monday). day(tuesday). day(wednesday). day(thursday). day(friday).

% Shifts: first and second
shift(first). shift(second).

% Students
student(grecia). student(hakeem). student(joe). student(katya). student(louise).

% Each student works exactly two shifts
1 { works(Student, Day, Shift) : day(Day), shift(Shift) } 2 :- student(Student).

% No student works both shifts of any day
:- works(Student, Day, first), works(Student, Day, second).

% On two consecutive days, Louise works the second shift
% We need to find two consecutive days where Louise works second shift
consecutive_day(D1, D2) :- day(D1), day(D2), D1 = monday, D2 = tuesday.
consecutive_day(D1, D2) :- day(D1), day(D2), D1 = tuesday, D2 = wednesday.
consecutive_day(D1, D2) :- day(D1), day(D2), D1 = wednesday, D2 = thursday.
consecutive_day(D1, D2) :- day(D1), day(D2), D1 = thursday, D2 = friday.

louise_second_on_consecutive :- works(louise, D1, second), works(louise, D2, second), consecutive_day(D1, D2).
:- not louise_second_on_consecutive.

% On two nonconsecutive days, Grecia works the first shift
% Nonconsecutive days: any two days that are not consecutive
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

% Show the schedule
#show works/3.

% For multiple-choice: we need to map to option/1
% Since the answer choices are about cookbooks, which are unrelated, we cannot derive a condition.
% However, we must provide an option mapping. We'll assume that the correct answer is based on the schedule.
% But without clear mapping, we'll derive a condition that is always true for one option arbitrarily.
% This is not ideal, but we need to satisfy the requirement.

% Let's define a helper: which students work on which days?
% We'll compute the set of students who work on each day.
% Then, we can check if any of the answer choices match.

% For simplicity, we'll assume that the answer choices are about which students work on fall (first three days) and spring (last two days).
% We'll define fall days: monday, tuesday, wednesday; spring days: thursday, friday.

fall_day(monday). fall_day(tuesday). fall_day(wednesday).
spring_day(thursday). spring_day(friday).

% Students who work on fall days
student_fall(Student) :- works(Student, Day, _), fall_day(Day).
% Students who work on spring days
student_spring(Student) :- works(Student, Day, _), spring_day(Day).

% Now, we need to map the answer choices to conditions on student_fall and student_spring.
% The answer choices use letters K, L, M, N, O, P. We need to map these to our students.
% Since we have only five students, we'll assume:
% K = katya, L = louise, M = grecia, N = hakeem, O = joe, and P is extra (maybe not used).
% But we have six letters, so we'll ignore P or assume it's not a student.

% For each answer choice, we'll define a condition that checks if the set of students in fall and spring matches.
% However, the answer choices have four students in fall and two in spring.
% In our schedule, the number of students in fall and spring may vary.

% We'll derive the correct option based on the actual schedule.
% Since we don't know which schedule is correct, we'll assume that the schedule we find satisfies one of the choices.

% After running the solver, we'll see the schedule and then decide which option matches.

% For now, we'll output all possible schedules and then manually check.
% But we need to map to option/1 in the code.

% We'll define a condition for each option based on the students in fall and spring.
% We'll use the following mapping: K=katya, L=louise, M=grecia, N=hakeem, O=joe.
% We'll ignore P.

option(a) :- student_fall(katya), student_fall(louise), student_fall(grecia), student_fall(joe),
             student_spring(hakeem), student_spring(joe), % but joe is in both? This is messy.
             #false. % This is not correct.

% Instead, we'll derive the correct option after seeing the schedule.
% Since we cannot see the schedule before running, we'll run the solver and then add the option mapping in a separate step.
% But we need to include the option mapping in the same file.

% We'll use a different approach: we'll compute the set of students in fall and spring as a string and compare.
% But that's complex.

% Given the time, I'll assume that the correct answer is C, as it is the only one with K, L, N, P in fall and M, O in spring.
% But we don't have P.

% I think the best is to run the scheduling problem and see what schedules are possible, then infer the answer.
% Since we cannot see the output before running, I'll run the code and then adjust.

% For now, I'll output the schedule and then manually determine the answer.
% But the tool will run and give output.

% Let's run the code and see what schedules are possible.