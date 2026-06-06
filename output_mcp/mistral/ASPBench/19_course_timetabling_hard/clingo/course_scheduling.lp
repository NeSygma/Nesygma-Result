% --- DOMAINS ---
course(0;1;2;3;4;5;6;7).
room(0;1;2;3).
time(0;1;2;3;4;5).
teacher(0;1;2;3;4).
department(sci;hum;eng).

% --- COURSE FACTS ---
course(0, 0, 30, sci).
course(1, 0, 25, sci).
course(2, 1, 40, sci).
course(3, 2, 50, hum).
course(4, 3, 45, hum).
course(5, 4, 60, eng).
course(6, 4, 55, eng).
course(7, 4, 50, eng).

% --- ROOM FACTS ---
% room(R, Capacity, Features) where Features is represented as separate facts
room(0, 60).
room(1, 50).
room(2, 40).
room(3, 30).

% Room features
room_feature(0, projector).
room_feature(1, projector).
room_feature(2, lab).
room_feature(2, projector).
% Room 3 has no features

% --- TEACHER FACTS ---
% Teacher availability: available(T, S) means teacher T is available at time S
% Teacher 0: slots [0,1,2]
available(0,0). available(0,1). available(0,2).
% Teacher 1: slots [2,3,4]
available(1,2). available(1,3). available(1,4).
% Teacher 2: slots [0,1,4,5]
available(2,0). available(2,1). available(2,4). available(2,5).
% Teacher 3: slots [0,2,3,5]
available(3,0). available(3,2). available(3,3). available(3,5).
% Teacher 4: slots [1,2,3,4,5]
available(4,1). available(4,2). available(4,3). available(4,4). available(4,5).

% --- PREREQUISITES ---
% C1 must be scheduled before C2
prereq(0, 1).  % Physics I before Physics II
prereq(5, 6).  % Intro Programming before Data Structures
prereq(6, 7).  % Data Structures before Algorithms

% --- STUDENT CONFLICTS ---
% C1 and C2 cannot be scheduled at the same time
conflict(1, 4).  % Physics II and Literature
conflict(2, 5).  % Chemistry and Intro Programming

% --- ROOM REQUIREMENTS ---
% Courses requiring specific features
requires_feature(2, lab).   % Chemistry requires lab
requires_feature(5, projector). % Intro Programming requires projector
requires_feature(6, projector). % Data Structures requires projector
requires_feature(7, projector). % Algorithms requires projector

% --- ASSIGNMENT CHOICE RULE ---
% Each course must be assigned to exactly one room and one time slot
1 { assigned(C, R, T) : room(R), time(T) } 1 :- course(C, _, _, _).

% --- CONSTRAINTS ---

% 1. Room capacity: course students <= room capacity
:- assigned(C, R, T), course(C, _, Students, _), room(R, Capacity), Students > Capacity.

% 2. Teacher availability: course can only be in teacher's available slots
:- assigned(C, R, T), course(C, Teacher, _, _), not available(Teacher, T).

% 3. Room features: courses requiring features must be in rooms with those features
:- assigned(C, R, T), requires_feature(C, F), not room_feature(R, F).

% 4. Prerequisites: C1 must be before C2
:- assigned(C1, R1, T1), assigned(C2, R2, T2), prereq(C1, C2), T1 >= T2.

% 5. Student conflicts: conflicting courses cannot be at same time
:- assigned(C1, R1, T), assigned(C2, R2, T), conflict(C1, C2).

% 6. Room uniqueness: no two courses in same room at same time
:- assigned(C1, R, T), assigned(C2, R, T), C1 != C2.

% 7. Teacher uniqueness: no two courses with same teacher at same time
:- assigned(C1, R1, T), assigned(C2, R2, T), course(C1, Teacher, _, _), course(C2, Teacher, _, _), C1 != C2.

% 8. Evening limit: max 2 courses in time slot 5
:- #count { C,R : assigned(C, R, 5) } > 2.

% --- COST CALCULATION ---
% Identify all courses scheduled at each time slot
scheduled_at(T, C) :- assigned(C, R, T).

% For each pair of consecutive time slots, check if they have same department
same_dept_adjacent(T) :- scheduled_at(T, C1), scheduled_at(T+1, C2), course(C1, _, _, Dept), course(C2, _, _, Dept), T < 5.

% Count the number of such adjacent pairs
cost(N) :- N = #count { T : same_dept_adjacent(T) }.

% --- MINIMIZE COST ---
#minimize { N : cost(N) }.

% --- SHOW DIRECTIVE ---
#show assigned/3.
#show cost/1.