% Domain definitions
exam(e1). exam(e2). exam(e3). exam(e4). exam(e5). exam(e6).
student(s1). student(s2). student(s3). student(s4).
timeslot(1). timeslot(2). timeslot(3).
room(r1). room(r2).

% Room capacities
capacity(r1, 3).
capacity(r2, 3).

% Student enrollments
enrolled(s1, e1). enrolled(s1, e3). enrolled(s1, e5).
enrolled(s2, e1). enrolled(s2, e4). enrolled(s2, e6).
enrolled(s3, e2). enrolled(s3, e3). enrolled(s3, e6).
enrolled(s4, e2). enrolled(s4, e4). enrolled(s4, e5).

% Each exam must be assigned to exactly one time slot and room
{ assign(E, T, R) : timeslot(T), room(R) } = 1 :- exam(E).

% Student conflict detection: student has conflict if they have two exams at same time slot
conflict(S, T) :- student(S), enrolled(S, E1), enrolled(S, E2), 
                  assign(E1, T, _), assign(E2, T, _), E1 != E2.

% Constraint: No student conflicts allowed
:- conflict(S, T).

% Count students per exam (each exam has exactly 2 students based on enrollments)
exam_student_count(E, 2) :- exam(E).

% Constraint: Room capacity not exceeded
:- assign(E, T, R), capacity(R, C), exam_student_count(E, N), N > C.

% Compute room utilization (number of exams per room)
room_utilization(R, N) :- room(R), N = #count{ E : assign(E, _, R) }.

% Output schedule in required format
schedule(E, 1, T, R, 1) :- assign(E, T, R).

% Conflicts resolved if no conflicts exist
conflicts_resolved :- not conflict(_, _).

% Show required outputs
#show schedule/5.
#show conflicts_resolved/0.
#show room_utilization/2.