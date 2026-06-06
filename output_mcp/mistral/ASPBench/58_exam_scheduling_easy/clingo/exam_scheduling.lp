% Domains
exam(e1; e2; e3; e4; e5; e6).
student(s1; s2; s3; s4).
room(r1; r2).
time_slot(1..3).

% Room capacities
capacity(r1, 3).
capacity(r2, 3).

% Enrollments
enrolled(s1, e1). enrolled(s1, e3). enrolled(s1, e5).
enrolled(s2, e1). enrolled(s2, e4). enrolled(s2, e6).
enrolled(s3, e2). enrolled(s3, e3). enrolled(s3, e6).
enrolled(s4, e2). enrolled(s4, e4). enrolled(s4, e5).

% Calculate number of students per exam
num_students(E, N) :- exam(E), N = #count { S : enrolled(S, E) }.

% Choice rule: schedule each exam to exactly one time slot and room
1 { scheduled(E, T, R) : time_slot(T), room(R) } 1 :- exam(E).

% Constraint: No student conflicts - a student cannot have two exams in the same time slot
:- enrolled(S, E1), enrolled(S, E2), E1 != E2,
   scheduled(E1, T, _), scheduled(E2, T, _).

% Constraint: Room capacity must not be exceeded
:- scheduled(E, T, R),
   capacity(R, MaxCapacity),
   num_students(E, NumStudents),
   NumStudents > MaxCapacity.

% Derive conflicts_resolved
conflicts_resolved :- not conflict_exists.
conflict_exists :- enrolled(S, E1), enrolled(S, E2), E1 != E2,
                  scheduled(E1, T, _), scheduled(E2, T, _).

% Derive room_utilization
room_utilization(R, N) :- room(R), N = #count { E : scheduled(E, _, R) }.

% Show the required predicates
#show scheduled/3.
#show conflicts_resolved/0.
#show room_utilization/2.