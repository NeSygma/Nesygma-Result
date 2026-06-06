% Domains
exam(e1). exam(e2). exam(e3). exam(e4). exam(e5). exam(e6). exam(e7). exam(e8).
student(s1). student(s2). student(s3). student(s4). student(s5). student(s6).
time(1..4).
room(r1). room(r2). room(r3).

% Room types and capacities
room_type(r1, classroom). room_capacity(r1,2).
room_type(r2, classroom). room_capacity(r2,2).
room_type(r3, lab). room_capacity(r3,2).

% Exam type requirements
exam_type(e1, classroom). exam_type(e2, classroom). exam_type(e3, classroom).
exam_type(e4, classroom). exam_type(e5, classroom). exam_type(e6, classroom).
exam_type(e7, lab). exam_type(e8, lab).

% Student enrollments
student_exam(s1,e1). student_exam(s1,e3). student_exam(s1,e7).
student_exam(s2,e2). student_exam(s2,e4). student_exam(s2,e8).
student_exam(s3,e1). student_exam(s3,e5).
student_exam(s4,e2). student_exam(s4,e6).
student_exam(s5,e3). student_exam(s5,e5). student_exam(s5,e8).
student_exam(s6,e4). student_exam(s6,e6). student_exam(s6,e7).

% Compute enrollment count per exam
enrollment(E,N) :- exam(E), N = #count { S : student_exam(S,E) }.

% Choice: assign each exam to exactly one time slot and one room
1 { assign(E,T,R) : time(T), room(R) } 1 :- exam(E).

% Constraint: student cannot have two exams at same time
:- student_exam(S,E1), student_exam(S,E2), E1 != E2, assign(E1,T,R1), assign(E2,T,R2).

% Constraint: room cannot host more than one exam at same time
:- assign(E1,T,R), assign(E2,T,R), E1 != E2.

% Constraint: room type must match exam type
:- assign(E,T,R), exam_type(E,Type), room_type(R,Rtype), Type != Rtype.

% Constraint: capacity
:- assign(E,T,R), enrollment(E,N), room_capacity(R,C), N > C.

#show assign/3.