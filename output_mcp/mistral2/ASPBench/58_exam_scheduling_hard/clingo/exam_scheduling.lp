% --- Facts ---
% Exams
exam(e1). exam(e2). exam(e3). exam(e4). exam(e5). exam(e6). exam(e7). exam(e8).

% Students
student(s1). student(s2). student(s3). student(s4). student(s5). student(s6).

% Time slots
time_slot(1). time_slot(2). time_slot(3). time_slot(4).

% Rooms
room(r1). room(r2). room(r3).

% Room types
room_type(r1, "classroom"). room_type(r2, "classroom"). room_type(r3, "lab").

% Room capacities (all 2)
room_capacity(r1, 2). room_capacity(r2, 2). room_capacity(r3, 2).

% Exam requirements
exam_requirement(e1, "classroom"). exam_requirement(e2, "classroom").
exam_requirement(e3, "classroom"). exam_requirement(e4, "classroom").
exam_requirement(e5, "classroom"). exam_requirement(e6, "classroom").
exam_requirement(e7, "lab"). exam_requirement(e8, "lab").

% Student enrollments
enrolled(s1, e1). enrolled(s1, e3). enrolled(s1, e7).
enrolled(s2, e2). enrolled(s2, e4). enrolled(s2, e8).
enrolled(s3, e1). enrolled(s3, e5).
enrolled(s4, e2). enrolled(s4, e6).
enrolled(s5, e3). enrolled(s5, e5). enrolled(s5, e8).
enrolled(s6, e4). enrolled(s6, e6). enrolled(s6, e7).

% --- Choice Rule ---
% Assign each exam to exactly one time slot and one room
{ scheduled(E, T, R) : time_slot(T), room(R) } = 1 :- exam(E).

% --- Constraints ---
% Student conflict: No student can be in two exams at the same time
:- enrolled(S, E1), enrolled(S, E2), E1 != E2, scheduled(E1, T, _), scheduled(E2, T, _).

% Room conflict: No room can host more than one exam in the same time slot
:- scheduled(E1, T, R), scheduled(E2, T, R), E1 != E2.

% Room type: Room type must match exam requirement
:- scheduled(E, T, R), exam_requirement(E, Type), room_type(R, OtherType), Type != OtherType.

% Room capacity: Number of students in an exam must not exceed room capacity
:- scheduled(E, _, R), room_capacity(R, C), #count { S : enrolled(S, E) } > C.

% --- Show Directive ---
#show scheduled/3.