% --- Domains ---
course(0..4).
room(0..2).
slot(0..3).

% --- Course Data ---
course_teacher(0,0). course_students(0,25).
course_teacher(1,1). course_students(1,20).
course_teacher(2,2). course_students(2,30).
course_teacher(3,1). course_students(3,15).
course_teacher(4,0). course_students(4,35).

% --- Room Data ---
room_capacity(0,40).
room_capacity(1,25).
room_capacity(2,20).

% --- Teacher Availability ---
teacher_available(0,0). teacher_available(0,1). teacher_available(0,2).
teacher_available(1,1). teacher_available(1,2). teacher_available(1,3).
teacher_available(2,0). teacher_available(2,2). teacher_available(2,3).

% --- Decision: Assign each course to a (room, slot) ---
{ assigned(C, R, S) : room(R), slot(S) } 1 :- course(C).

% Constraint 1: Each course scheduled exactly once
:- course(C), not assigned(C, _, _).

% Constraint 2: No two courses in same room at same time
:- assigned(C1, R, S), assigned(C2, R, S), C1 != C2.

% Constraint 3: Teacher cannot teach two courses simultaneously
:- assigned(C1, _, S), assigned(C2, _, S), C1 != C2,
   course_teacher(C1, T), course_teacher(C2, T).

% Constraint 4: Room capacity must accommodate course enrollment
:- assigned(C, R, _), course_students(C, N), room_capacity(R, Cap), N > Cap.

% Constraint 5: Course only when teacher is available
:- assigned(C, _, S), course_teacher(C, T), not teacher_available(T, S).

% --- Show the assignment ---
#show assigned/3.