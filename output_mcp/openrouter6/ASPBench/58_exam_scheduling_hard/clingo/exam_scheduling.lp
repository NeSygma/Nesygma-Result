% Exam Scheduling Problem
% =========================

% --- Domain Declarations ---
exam(E) :- E = 1..8.  % E1-E8
student(S) :- S = 1..6.  % S1-S6
time(T) :- T = 1..4.  % Time slots 1-4
room(R) :- R = 1..3.  % Rooms R1-R3

% --- Room Properties ---
% R1: classroom, capacity 2
% R2: classroom, capacity 2  
% R3: lab, capacity 2
room_type(1, classroom). room_capacity(1, 2).
room_type(2, classroom). room_capacity(2, 2).
room_type(3, lab).       room_capacity(3, 2).

% --- Exam Requirements ---
% Classroom required: E1, E2, E3, E4, E5, E6
% Lab required: E7, E8
exam_requires_type(E, classroom) :- E = 1..6.
exam_requires_type(E, lab) :- E = 7..8.

% --- Student Enrollments ---
% S1: E1, E3, E7
enrolled(1, 1). enrolled(1, 3). enrolled(1, 7).
% S2: E2, E4, E8
enrolled(2, 2). enrolled(2, 4). enrolled(2, 8).
% S3: E1, E5
enrolled(3, 1). enrolled(3, 5).
% S4: E2, E6
enrolled(4, 2). enrolled(4, 6).
% S5: E3, E5, E8
enrolled(5, 3). enrolled(5, 5). enrolled(5, 8).
% S6: E4, E6, E7
enrolled(6, 4). enrolled(6, 6). enrolled(6, 7).

% --- Assignment Decision Variables ---
% Each exam assigned to exactly one time slot and one room
{ assignment(E, T, R) : time(T), room(R) } 1 :- exam(E).

% --- Constraint 1: Room Conflict ---
% A room cannot host more than one exam in the same time slot
:- assignment(E1, T, R), assignment(E2, T, R), E1 != E2.

% --- Constraint 2: Student Conflict ---
% A student cannot be scheduled for two different exams in the same time slot
% Derive student exam times from assignments and enrollments
student_exam_time(S, E, T) :- enrolled(S, E), assignment(E, T, _).
:- student_exam_time(S, E1, T), student_exam_time(S, E2, T), E1 != E2.

% --- Constraint 3: Room Type ---
% An exam must be scheduled in a room that matches its required type
:- assignment(E, T, R), exam_requires_type(E, TypeReq), room_type(R, TypeRoom), TypeReq != TypeRoom.

% --- Constraint 4: Room Capacity ---
% The number of students enrolled in an exam cannot exceed room capacity
% Count students per exam
exam_student_count(E, N) :- exam(E), N = #count{ S : enrolled(S, E) }.
% Check capacity constraint
:- assignment(E, T, R), exam_student_count(E, N), room_capacity(R, Cap), N > Cap.

% --- Output ---
#show assignment/3.
#show exam_student_count/2.