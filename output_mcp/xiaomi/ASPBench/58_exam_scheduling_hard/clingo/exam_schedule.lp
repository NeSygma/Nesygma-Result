% ==============================
% Domain Facts
% ==============================

% Exams
exam(e1). exam(e2). exam(e3). exam(e4). exam(e5). exam(e6). exam(e7). exam(e8).

% Students
student(s1). student(s2). student(s3). student(s4). student(s5). student(s6).

% Time Slots
time_slot(1). time_slot(2). time_slot(3). time_slot(4).

% Rooms
room(r1). room(r2). room(r3).

% Room Types
room_type(r1, classroom).
room_type(r2, classroom).
room_type(r3, lab).

% Room Capacities
capacity(r1, 2).
capacity(r2, 2).
capacity(r3, 2).

% Student Enrollments
enrolled(s1, e1). enrolled(s1, e3). enrolled(s1, e7).
enrolled(s2, e2). enrolled(s2, e4). enrolled(s2, e8).
enrolled(s3, e1). enrolled(s3, e5).
enrolled(s4, e2). enrolled(s4, e6).
enrolled(s5, e3). enrolled(s5, e5). enrolled(s5, e8).
enrolled(s6, e4). enrolled(s6, e6). enrolled(s6, e7).

% Exam Room Type Requirements
exam_type(e1, classroom).
exam_type(e2, classroom).
exam_type(e3, classroom).
exam_type(e4, classroom).
exam_type(e5, classroom).
exam_type(e6, classroom).
exam_type(e7, lab).
exam_type(e8, lab).

% ==============================
% Derived Facts
% ==============================

% Count enrollment per exam
enrollment_count(E, N) :- exam(E), N = #count{S : enrolled(S, E)}.

% ==============================
% Choice Rule: Schedule each exam
% ==============================

% Each exam must be assigned to exactly one time slot and one room
1 { scheduled(E, T, R) : time_slot(T), room(R) } 1 :- exam(E).

% ==============================
% Constraints
% ==============================

% Constraint 2: Student Conflict - no student has two exams in same time slot
:- student(S), time_slot(T), exam(E1), exam(E2), E1 != E2,
   enrolled(S, E1), enrolled(S, E2),
   scheduled(E1, T, _), scheduled(E2, T, _).

% Constraint 3: Room Conflict - no room hosts two exams in same time slot
:- room(R), time_slot(T), exam(E1), exam(E2), E1 != E2,
   scheduled(E1, T, R), scheduled(E2, T, R).

% Constraint 4: Room Type - exam must be in matching room type
:- exam(E), time_slot(T), room(R),
   scheduled(E, T, R),
   exam_type(E, ReqType),
   room_type(R, RoomType),
   ReqType != RoomType.

% Constraint 5: Room Capacity - enrollment count must not exceed capacity
:- exam(E), time_slot(T), room(R),
   scheduled(E, T, R),
   enrollment_count(E, N),
   capacity(R, Cap),
   N > Cap.

% ==============================
% Output
% ==============================

#show scheduled/3.
#show status/1.

% Show status
status(satisfiable).