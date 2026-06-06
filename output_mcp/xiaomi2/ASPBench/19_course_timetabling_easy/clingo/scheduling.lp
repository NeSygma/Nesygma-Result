% ===== Domain Facts =====
% Courses
course(0). course(1). course(2). course(3). course(4).

% Rooms
room(0). room(1). room(2).

% Time Slots
slot(0). slot(1). slot(2). slot(3).

% Teachers
teacher(0). teacher(1). teacher(2).

% ===== Course Data =====
% teaches(Teacher, Course)
teaches(0, 0).  % Teacher 0 teaches Math
teaches(1, 1).  % Teacher 1 teaches Physics
teaches(2, 2).  % Teacher 2 teaches Chemistry
teaches(1, 3).  % Teacher 1 teaches Biology
teaches(0, 4).  % Teacher 0 teaches Computer Science

% students(Course, NumStudents)
students(0, 25).  % Math: 25 students
students(1, 20).  % Physics: 20 students
students(2, 30).  % Chemistry: 30 students
students(3, 15).  % Biology: 15 students
students(4, 35).  % Computer Science: 35 students

% ===== Room Data =====
% capacity(Room, Capacity)
capacity(0, 40).  % Room 0: capacity 40
capacity(1, 25).  % Room 1: capacity 25
capacity(2, 20).  % Room 2: capacity 20

% ===== Teacher Availability =====
% available(Teacher, Slot)
available(0, 0). available(0, 1). available(0, 2).  % Teacher 0: slots 0,1,2
available(1, 1). available(1, 2). available(1, 3).  % Teacher 1: slots 1,2,3
available(2, 0). available(2, 2). available(2, 3).  % Teacher 2: slots 0,2,3

% ===== Decision Variable =====
% assign(Course, Room, Slot) - course C assigned to room R at slot S
% Constraint 1: Each course must be scheduled exactly once
1 { assign(C, R, S) : room(R), slot(S) } 1 :- course(C).

% ===== Constraints =====

% Constraint 2: No two courses can use the same room at the same time
:- assign(C1, R, S), assign(C2, R, S), C1 != C2.

% Constraint 3: Teachers cannot teach multiple courses simultaneously
:- assign(C1, _, S), assign(C2, _, S), C1 != C2, teaches(T, C1), teaches(T, C2).

% Constraint 4: Room capacity must accommodate course enrollment
:- assign(C, R, _), students(C, N), capacity(R, M), N > M.

% Constraint 5: Courses can only be scheduled when their teacher is available
:- assign(C, _, S), teaches(T, C), not available(T, S).

% ===== Display =====
#show assign/3.