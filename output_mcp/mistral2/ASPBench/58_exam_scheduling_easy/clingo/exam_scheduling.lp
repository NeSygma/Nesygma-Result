% --- Domains ---
exam(e1; e2; e3; e4; e5; e6).
student(s1; s2; s3; s4).
time_slot(1..3).
room(r1; r2).

% --- Enrollments ---
enrolled(s1, e1). enrolled(s1, e3). enrolled(s1, e5).
enrolled(s2, e1). enrolled(s2, e4). enrolled(s2, e6).
enrolled(s3, e2). enrolled(s3, e3). enrolled(s3, e6).
enrolled(s4, e2). enrolled(s4, e4). enrolled(s4, e5).

% --- Room Capacities ---
room_capacity(r1, 3). room_capacity(r2, 3).

% --- Schedule Assignment ---
{ scheduled(E, T, R) : time_slot(T), room(R) } = 1 :- exam(E).

% --- Student Conflicts ---
% A student cannot have two exams in the same time slot.
:- enrolled(S, E1), enrolled(S, E2), E1 < E2,
   scheduled(E1, T, _), scheduled(E2, T, _).

% --- Room Capacity ---
% The number of students in an exam must not exceed the room capacity.
student_count(E, N) :- exam(E),
    N = #count { S : enrolled(S, E) }.
:- scheduled(E, _, R), student_count(E, N),
   room_capacity(R, C), N > C.

% --- Show the schedule ---
#show scheduled/3.