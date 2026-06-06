% University Course Scheduling Problem

% Domain declarations
course(0..4).
room(0..2).
time(0..3).

% Teacher assignments per course
teacher(0, 0).  % Math -> Teacher 0
teacher(1, 1).  % Physics -> Teacher 1
teacher(2, 2).  % Chemistry -> Teacher 2
teacher(3, 1).  % Biology -> Teacher 1
teacher(4, 0).  % Computer Science -> Teacher 0

% Student counts per course
students(0, 25).
students(1, 20).
students(2, 30).
students(3, 15).
students(4, 35).

% Room capacities
capacity(0, 40).
capacity(1, 25).
capacity(2, 20).

% Teacher availability (teacher, time slot)
available(0, 0). available(0, 1). available(0, 2).  % Teacher 0: slots 0,1,2
available(1, 1). available(1, 2). available(1, 3).  % Teacher 1: slots 1,2,3
available(2, 0). available(2, 2). available(2, 3).  % Teacher 2: slots 0,2,3

% Decision: schedule each course exactly once in a room and time slot
1 { scheduled(C, R, T) : room(R), time(T) } 1 :- course(C).

% Constraint 1: No two courses can use the same room at the same time
:- scheduled(C1, R, T), scheduled(C2, R, T), C1 != C2.

% Constraint 2: Teachers cannot teach multiple courses simultaneously
:- scheduled(C1, R1, T), scheduled(C2, R2, T), 
   teacher(C1, Tchr), teacher(C2, Tchr), C1 != C2.

% Constraint 3: Room capacity must accommodate course enrollment
:- scheduled(C, R, T), students(C, S), capacity(R, Cap), S > Cap.

% Constraint 4: Courses can only be scheduled when their teacher is available
:- scheduled(C, R, T), teacher(C, Tchr), not available(Tchr, T).

% Show the solution
#show scheduled/3.