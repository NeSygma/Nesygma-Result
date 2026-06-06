% Course Scheduling Problem

% ===== DOMAIN DECLARATIONS =====
course(0..7).
room(0..3).
time(0..5).
teacher(0..4).
dept("sci"; "hum"; "eng").

% ===== COURSE DATA =====
teacher(0, 0). students(0, 30). dept(0, "sci").
teacher(1, 0). students(1, 25). dept(1, "sci").
teacher(2, 1). students(2, 40). dept(2, "sci").
teacher(3, 2). students(3, 50). dept(3, "hum").
teacher(4, 3). students(4, 45). dept(4, "hum").
teacher(5, 4). students(5, 60). dept(5, "eng").
teacher(6, 4). students(6, 55). dept(6, "eng").
teacher(7, 4). students(7, 50). dept(7, "eng").

% ===== ROOM DATA =====
capacity(0, 60). feature(0, "projector").
capacity(1, 50). feature(1, "projector").
capacity(2, 40). feature(2, "lab"). feature(2, "projector").
capacity(3, 30).

% ===== TEACHER AVAILABILITY =====
teacher_available(0, 0). teacher_available(0, 1). teacher_available(0, 2).
teacher_available(1, 2). teacher_available(1, 3). teacher_available(1, 4).
teacher_available(2, 0). teacher_available(2, 1). teacher_available(2, 4). teacher_available(2, 5).
teacher_available(3, 0). teacher_available(3, 2). teacher_available(3, 3). teacher_available(3, 5).
teacher_available(4, 1). teacher_available(4, 2). teacher_available(4, 3). teacher_available(4, 4). teacher_available(4, 5).

% ===== ROOM REQUIREMENTS =====
room_requirement(2, "lab").      % Chemistry requires lab
room_requirement(5, "projector"). % Intro Programming requires projector
room_requirement(6, "projector"). % Data Structures requires projector
room_requirement(7, "projector"). % Algorithms requires projector

% ===== PREREQUISITES =====
prerequisite(0, 1).  % Physics I before Physics II
prerequisite(5, 6).  % Intro Programming before Data Structures
prerequisite(6, 7).  % Data Structures before Algorithms

% ===== STUDENT CONFLICTS =====
conflict(1, 4).  % Physics II and Literature
conflict(2, 5).  % Chemistry and Intro Programming

% ===== MAIN DECISION: ASSIGNMENT =====
% Each course assigned to exactly one room and one time slot
1 { assignment(C, R, T) : room(R), time(T) } 1 :- course(C).

% ===== CONSTRAINTS =====

% 1. Room Uniqueness: No two courses in same room at same time
:- assignment(C1, R, T), assignment(C2, R, T), C1 != C2.

% 2. Teacher Uniqueness: No two courses by same teacher at same time
:- assignment(C1, R1, T), assignment(C2, R2, T), 
   teacher(C1, Tchr), teacher(C2, Tchr), C1 != C2.

% 3. Room Capacity: Course students <= room capacity
:- assignment(C, R, T), students(C, S), capacity(R, Cap), S > Cap.

% 4. Teacher Availability: Course time must be available for teacher
:- assignment(C, R, T), teacher(C, Tchr), not teacher_available(Tchr, T).

% 5. Room Features: Course requirements must be met by room
:- assignment(C, R, T), room_requirement(C, F), not feature(R, F).

% 6. Prerequisites: Prerequisite must be before dependent
:- assignment(C1, R1, T1), assignment(C2, R2, T2), 
   prerequisite(C1, C2), T1 >= T2.

% 7. Student Conflicts: Conflicting courses cannot be at same time
:- assignment(C1, R1, T), assignment(C2, R2, T), 
   conflict(C1, C2), C1 != C2.

% 8. Global Evening Limit: Max 2 courses in time slot 5
:- N = #count{ C : assignment(C, _, 5) }, N > 2.

% ===== OBJECTIVE: MINIMIZE ADJACENT SAME-DEPARTMENT PAIRS =====
% Define adjacent same-department pairs
adjacent_same_dept(C1, C2, T) :- 
    assignment(C1, R1, T), assignment(C2, R2, T+1),
    dept(C1, D), dept(C2, D), C1 != C2.

% Count total cost
cost(N) :- N = #count{ C1, C2, T : adjacent_same_dept(C1, C2, T) }.

% ===== SHOW DIRECTIVES =====
#show assignment/3.
#show cost/1.
#show adjacent_same_dept/3.

% ===== OPTIMIZATION =====
#minimize { 1, C1, C2, T : adjacent_same_dept(C1, C2, T) }.