% ===== DOMAIN FACTS =====
% Courses
course(0). course(1). course(2). course(3). course(4).

% Rooms
room(0). room(1). room(2).

% Time slots
slot(0). slot(1). slot(2). slot(3).

% Teachers
teacher(0). teacher(1). teacher(2).

% ===== INSTANCE DATA =====
% Teacher assignments to courses
teaches(0, 0).  % Math taught by teacher 0
teaches(1, 1).  % Physics taught by teacher 1
teaches(2, 2).  % Chemistry taught by teacher 2
teaches(3, 1).  % Biology taught by teacher 1
teaches(4, 0).  % Computer Science taught by teacher 0

% Student enrollment per course
students(0, 25).  % Math
students(1, 20).  % Physics
students(2, 30).  % Chemistry
students(3, 15).  % Biology
students(4, 35).  % Computer Science

% Room capacities
capacity(0, 40).  % Room 0
capacity(1, 25).  % Room 1
capacity(2, 20).  % Room 2

% Teacher availability
available(0, 0).  % Teacher 0 available slot 0
available(0, 1).  % Teacher 0 available slot 1
available(0, 2).  % Teacher 0 available slot 2
available(1, 1).  % Teacher 1 available slot 1
available(1, 2).  % Teacher 1 available slot 2
available(1, 3).  % Teacher 1 available slot 3
available(2, 0).  % Teacher 2 available slot 0
available(2, 2).  % Teacher 2 available slot 2
available(2, 3).  % Teacher 2 available slot 3

% ===== CHOICE RULE =====
% Each course must be assigned to exactly one (room, slot) pair
1 { assigned(C, R, T) : room(R), slot(T) } 1 :- course(C).

% ===== CONSTRAINTS =====

% Constraint 1: No two courses in the same room at the same time
:- assigned(C1, R, T), assigned(C2, R, T), C1 != C2.

% Constraint 2: Teachers cannot teach multiple courses simultaneously
:- assigned(C1, R1, T), assigned(C2, R2, T), C1 != C2, teaches(C1, Teacher), teaches(C2, Teacher).

% Constraint 3: Room capacity must accommodate course enrollment
:- assigned(C, R, T), students(C, N), capacity(R, Cap), N > Cap.

% Constraint 4: Courses can only be scheduled when their teacher is available
:- assigned(C, R, T), teaches(C, Teacher), not available(Teacher, T).

% ===== OUTPUT =====
#show assigned/3.