% University Course Scheduling Problem

% Domain declarations
course(0..4).
room(0..2).
time(0..3).

% Course properties
teacher(0, 0). students(0, 25).  % Math, teacher 0, 25 students
teacher(1, 1). students(1, 20).  % Physics, teacher 1, 20 students
teacher(2, 2). students(2, 30).  % Chemistry, teacher 2, 30 students
teacher(3, 1). students(3, 15).  % Biology, teacher 1, 15 students
teacher(4, 0). students(4, 35).  % Computer Science, teacher 0, 35 students

% Room capacities
capacity(0, 40).
capacity(1, 25).
capacity(2, 20).

% Teacher availability
available(0, 0). available(0, 1). available(0, 2).  % Teacher 0: slots 0,1,2
available(1, 1). available(1, 2). available(1, 3).  % Teacher 1: slots 1,2,3
available(2, 0). available(2, 2). available(2, 3).  % Teacher 2: slots 0,2,3

% Choice rule: Each course scheduled exactly once in some (room, time) pair
1 { scheduled(C, R, T) : room(R), time(T) } 1 :- course(C).

% Constraint 1: No two courses in same room at same time
:- scheduled(C1, R, T), scheduled(C2, R, T), C1 != C2.

% Constraint 2: Teachers cannot teach multiple courses simultaneously
:- scheduled(C1, R, T), scheduled(C2, R2, T), 
   teacher(C1, Tchr), teacher(C2, Tchr), C1 != C2.

% Constraint 3: Room capacity must accommodate course enrollment
:- scheduled(C, R, T), students(C, S), capacity(R, Cap), S > Cap.

% Constraint 4: Courses only scheduled when teacher is available
:- scheduled(C, R, T), teacher(C, Tchr), not available(Tchr, T).

% Show solution
solution_exists :- scheduled(_, _, _).
#show solution_exists.
#show scheduled/3.