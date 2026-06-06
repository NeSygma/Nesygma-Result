% Exam Scheduling Problem

% Domain declarations
exam(E) :- E = 1..8.
student(S) :- S = 1..6.
time(T) :- T = 1..4.
room(R) :- R = 1..3.

% Room types and capacities
room_type(1, classroom). room_capacity(1, 2).
room_type(2, classroom). room_capacity(2, 2).
room_type(3, lab). room_capacity(3, 2).

% Student enrollments
enrolled(1, 1). enrolled(1, 3). enrolled(1, 7).
enrolled(2, 2). enrolled(2, 4). enrolled(2, 8).
enrolled(3, 1). enrolled(3, 5).
enrolled(4, 2). enrolled(4, 6).
enrolled(5, 3). enrolled(5, 5). enrolled(5, 8).
enrolled(6, 4). enrolled(6, 6). enrolled(6, 7).

% Exam room type requirements
exam_requires(1, classroom). exam_requires(2, classroom).
exam_requires(3, classroom). exam_requires(4, classroom).
exam_requires(5, classroom). exam_requires(6, classroom).
exam_requires(7, lab). exam_requires(8, lab).

% Calculate number of students per exam
student_count(E, N) :- exam(E), N = #count{S : enrolled(S, E)}.

% Assignment choice rule: each exam assigned to exactly one time slot and room
1 { assign(E, T, R) : time(T), room(R) } 1 :- exam(E).

% Constraint 1: Room type must match exam requirement
:- assign(E, T, R), exam_requires(E, Type), room_type(R, Type2), Type != Type2.

% Constraint 2: Room capacity constraint
:- assign(E, T, R), student_count(E, N), room_capacity(R, Cap), N > Cap.

% Constraint 3: No student conflict (same student in two exams same time)
:- assign(E1, T, R1), assign(E2, T, R2), E1 != E2,
   enrolled(S, E1), enrolled(S, E2).

% Constraint 4: No room conflict (same room hosting two exams same time)
:- assign(E1, T, R), assign(E2, T, R), E1 != E2.

% Show the schedule
#show assign/3.
#show student_count/2.