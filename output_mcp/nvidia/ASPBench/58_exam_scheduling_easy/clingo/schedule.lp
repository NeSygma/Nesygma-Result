% Domain definitions
exam(e1). exam(e2). exam(e3). exam(e4). exam(e5). exam(e6).
student(s1). student(s2). student(s3). student(s4).
room(r1). room(r2).
timeslot(1). timeslot(2). timeslot(3).

% Enrollment facts
enroll(s1, e1). enroll(s1, e3). enroll(s1, e5).
enroll(s2, e1). enroll(s2, e4). enroll(s2, e6).
enroll(s3, e2). enroll(s3, e3). enroll(s3, e6).
enroll(s4, e2). enroll(s4, e4). enroll(s4, e5).

% Room capacities
capacity(r1, 3). capacity(r2, 3).

% Helper predicate: enrollment count per exam
enrol_cnt(E, N) :- exam(E), #count{ S : enroll(E, S) } = N.

% Schedule: each exam assigned to exactly one (time_slot, room)
{ schedule(E, T, R) : timeslot(T), room(R) } 1 :- exam(E).

% No student conflicts: a student cannot have two exams at the same time slot
:- student(S), schedule(E1, T, R1), schedule(E2, T, R2), enroll(S, E1), enroll(S, E2), E1 != E2.

% Capacity constraint: number of enrolled students must not exceed room capacity
:- schedule(E, T, R), enrol_cnt(E, N), capacity(R, C), N > C.

% Show the schedule
#show schedule/3.