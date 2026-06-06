% Domains
course(0..4).
room(0..2).
time(0..3).
teacher(0..2).

% Course properties
course_name(0, "Math").
course_name(1, "Physics").
course_name(2, "Chemistry").
course_name(3, "Biology").
course_name(4, "Computer Science").

course_teacher(0, 0).
course_teacher(1, 1).
course_teacher(2, 2).
course_teacher(3, 1).
course_teacher(4, 0).

course_students(0, 25).
course_students(1, 20).
course_students(2, 30).
course_students(3, 15).
course_students(4, 35).

% Room capacities
room_capacity(0, 40).
room_capacity(1, 25).
room_capacity(2, 20).

% Teacher availability
teacher_available(0, 0).
teacher_available(0, 1).
teacher_available(0, 2).

teacher_available(1, 1).
teacher_available(1, 2).
teacher_available(1, 3).

teacher_available(2, 0).
teacher_available(2, 2).
teacher_available(2, 3).

% Choice rule: assign each course to a room and time slot
{ assigned(C, R, T) : room(R), time(T) } 1 :- course(C).

% Constraint 2: No two courses in same room at same time
:- assigned(C1, R, T), assigned(C2, R, T), C1 != C2.

% Constraint 3: Teachers cannot teach multiple courses simultaneously
:- assigned(C1, _, T), assigned(C2, _, T), C1 != C2,
   course_teacher(C1, Teach), course_teacher(C2, Teach).

% Constraint 4: Room capacity must accommodate course enrollment
:- assigned(C, R, T), course_students(C, Size), room_capacity(R, Cap), Size > Cap.

% Constraint 5: Courses can only be scheduled when teacher is available
:- assigned(C, _, T), course_teacher(C, Teach), not teacher_available(Teach, T).

% Show the solution
#show assigned/3.