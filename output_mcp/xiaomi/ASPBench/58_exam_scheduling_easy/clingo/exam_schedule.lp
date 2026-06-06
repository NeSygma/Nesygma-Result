% ==================== DOMAIN FACTS ====================
% Exams
exam(e1). exam(e2). exam(e3). exam(e4). exam(e5). exam(e6).

% Students
student(s1). student(s2). student(s3). student(s4).

% Rooms
room(r1). room(r2).

% Time slots (3 available)
slot(1). slot(2). slot(3).

% Room capacities
capacity(r1, 3).
capacity(r2, 3).

% Student enrollments
enrolled(s1, e1). enrolled(s1, e3). enrolled(s1, e5).
enrolled(s2, e1). enrolled(s2, e4). enrolled(s2, e6).
enrolled(s3, e2). enrolled(s3, e3). enrolled(s3, e6).
enrolled(s4, e2). enrolled(s4, e4). enrolled(s4, e5).

% ==================== DERIVED FACTS ====================
% Count students per exam
exam_size(E, N) :- exam(E), N = #count{S : student(S), enrolled(S, E)}.

% ==================== CHOICE RULES ====================
% Each exam must be assigned to exactly one time slot and room
1 { assigned(E, T, R) : slot(T), room(R) } 1 :- exam(E).

% ==================== CONSTRAINTS ====================
% Constraint 1: No student conflicts - a student cannot have two exams at the same time slot
:- student(S), enrolled(S, E1), enrolled(S, E2), E1 < E2,
   assigned(E1, T, _), assigned(E2, T, _).

% Constraint 2: Room capacity - number of students in an exam must not exceed room capacity
:- assigned(E, _, R), exam_size(E, N), capacity(R, C), N > C.

% ==================== OUTPUT PREDICATES ====================
% Check if all conflicts are resolved (always true if solver finds a solution)
conflicts_resolved.

% Room utilization: count exams per room
room_utilization(R, N) :- room(R), N = #count{E : assigned(E, _, R)}.

% ==================== SHOW DIRECTIVES ====================
#show assigned/3.
#show conflicts_resolved/0.
#show room_utilization/2.
#show exam_size/2.