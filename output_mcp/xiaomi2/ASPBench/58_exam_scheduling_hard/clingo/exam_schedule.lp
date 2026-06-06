% ===== DOMAIN DEFINITIONS =====
exam(e1). exam(e2). exam(e3). exam(e4). exam(e5). exam(e6). exam(e7). exam(e8).
student(s1). student(s2). student(s3). student(s4). student(s5). student(s6).
time_slot(1). time_slot(2). time_slot(3). time_slot(4).
room(r1). room(r2). room(r3).

% ===== ROOM TYPES =====
room_type(r1, classroom).
room_type(r2, classroom).
room_type(r3, lab).

% ===== ROOM CAPACITIES =====
room_capacity(r1, 2).
room_capacity(r2, 2).
room_capacity(r3, 2).

% ===== EXAM ROOM TYPE REQUIREMENTS =====
exam_type(e1, classroom).
exam_type(e2, classroom).
exam_type(e3, classroom).
exam_type(e4, classroom).
exam_type(e5, classroom).
exam_type(e6, classroom).
exam_type(e7, lab).
exam_type(e8, lab).

% ===== STUDENT ENROLLMENTS =====
enrolled(s1, e1). enrolled(s1, e3). enrolled(s1, e7).
enrolled(s2, e2). enrolled(s2, e4). enrolled(s2, e8).
enrolled(s3, e1). enrolled(s3, e5).
enrolled(s4, e2). enrolled(s4, e6).
enrolled(s5, e3). enrolled(s5, e5). enrolled(s5, e8).
enrolled(s6, e4). enrolled(s6, e6). enrolled(s6, e7).

% ===== DERIVED: COUNT STUDENTS PER EXAM =====
students_in_exam(E, N) :- exam(E), N = #count{S : enrolled(S, E)}.

% ===== CONSTRAINT 1: COMPLETE SCHEDULING =====
% Each exam must be assigned to exactly one time slot and one room.
% Constrain choice to valid room-type matches (Constraint 4 baked in).
{ assign(E, T, R) : time_slot(T), room(R), room_type(R, RT), exam_type(E, RT) } 1 :- exam(E).

% ===== CONSTRAINT 2: STUDENT CONFLICT =====
% A student cannot have two different exams in the same time slot.
:- enrolled(S, Ea), enrolled(S, Eb), Ea != Eb, assign(Ea, T, _), assign(Eb, T, _).

% ===== CONSTRAINT 3: ROOM CONFLICT =====
% A room cannot host more than one exam in the same time slot.
:- assign(Ea, T, R), assign(Eb, T, R), Ea != Eb.

% ===== CONSTRAINT 5: ROOM CAPACITY =====
% Number of students enrolled in an exam cannot exceed room capacity.
:- assign(E, _, R), students_in_exam(E, N), room_capacity(R, Cap), N > Cap.

% ===== OUTPUT =====
#show assign/3.