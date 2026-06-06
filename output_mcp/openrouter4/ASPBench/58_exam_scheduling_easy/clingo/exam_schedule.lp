% --- Domains ---
exam(e1;e2;e3;e4;e5;e6).
student(s1;s2;s3;s4).
room(r1;r2).
slot(1..3).

% --- Enrollments ---
enrolled(s1,e1). enrolled(s1,e3). enrolled(s1,e5).
enrolled(s2,e1). enrolled(s2,e4). enrolled(s2,e6).
enrolled(s3,e2). enrolled(s3,e3). enrolled(s3,e6).
enrolled(s4,e2). enrolled(s4,e4). enrolled(s4,e5).

% --- Room capacities ---
capacity(r1,3).
capacity(r2,3).

% --- Compute exam sizes (number of enrolled students) ---
exam_size(E, N) :- exam(E), N = #count{ S : enrolled(S, E) }.

% --- Assignment: each exam gets exactly one slot and one room ---
1 { assigned(E, T, R) : slot(T), room(R) } 1 :- exam(E).

% --- Constraint: Each (slot, room) gets at most one exam ---
:- assigned(E1, T, R), assigned(E2, T, R), E1 < E2.

% --- Constraint: No student conflicts at same slot ---
% If a student is enrolled in two exams, those exams cannot be at the same time slot.
:- enrolled(S, E1), enrolled(S, E2), E1 < E2,
   assigned(E1, T, _), assigned(E2, T, _).

% --- Constraint: Room capacity must not be exceeded ---
:- assigned(E, _, R), exam_size(E, N), capacity(R, C), N > C.

% --- Derive schedule facts (day=1 for all, duration=1 for all) ---
scheduled(E, 1, T, R, 1) :- assigned(E, T, R).

% --- Conflicts resolved (true if this model exists) ---
conflicts_resolved(true).

% --- Room utilization: count exams per room ---
room_utilization(R, N) :- room(R), N = #count{ E, T : assigned(E, T, R) }.

% --- Show output ---
#show scheduled/5.
#show conflicts_resolved/1.
#show room_utilization/2.