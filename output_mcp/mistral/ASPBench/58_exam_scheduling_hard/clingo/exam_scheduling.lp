% Define the domain
% Exams
exam(e1). exam(e2). exam(e3). exam(e4). exam(e5). exam(e6). exam(e7). exam(e8).

% Students
student(s1). student(s2). student(s3). student(s4). student(s5). student(s6).

% Time slots
time(1..4).

% Rooms
room(r1). room(r2). room(r3).

% Room properties
room_type(r1, classroom). room_type(r2, classroom). room_type(r3, lab).
room_capacity(r1, 2). room_capacity(r2, 2). room_capacity(r3, 2).

% Exam requirements
exam_required_type(e1, classroom). exam_required_type(e2, classroom).
exam_required_type(e3, classroom). exam_required_type(e4, classroom).
exam_required_type(e5, classroom). exam_required_type(e6, classroom).
exam_required_type(e7, lab). exam_required_type(e8, lab).

% Student enrollments
enrolled(s1, e1). enrolled(s1, e3). enrolled(s1, e7).
enrolled(s2, e2). enrolled(s2, e4). enrolled(s2, e8).
enrolled(s3, e1). enrolled(s3, e5).
enrolled(s4, e2). enrolled(s4, e6).
enrolled(s5, e3). enrolled(s5, e5). enrolled(s5, e8).
enrolled(s6, e4). enrolled(s6, e6). enrolled(s6, e7).

% Choice rule: Assign each exam to a time slot and a room
{ assignment(Exam, Time, Room) : time(Time), room(Room) } = 1 :- exam(Exam).

% Constraint 1: Room type must match exam requirement
:- assignment(Exam, Time, Room), exam_required_type(Exam, Type), room_type(Room, RoomType), Type != RoomType.

% Constraint 2: Room capacity must be >= number of students enrolled in the exam
:- assignment(Exam, Time, Room), room_capacity(Room, Capacity),
   #count { S : enrolled(S, Exam) } > Capacity.

% Constraint 3: No student conflict (a student cannot have two exams in the same time slot)
:- student(S), time(T), exam(E1), exam(E2), E1 != E2,
   enrolled(S, E1), enrolled(S, E2), assignment(E1, T, _), assignment(E2, T, _).

% Constraint 4: No room conflict (a room cannot host more than one exam in the same time slot)
:- time(T), room(R), exam(E1), exam(E2), E1 != E2,
   assignment(E1, T, R), assignment(E2, T, R).

% Show the schedule
#show assignment/3.