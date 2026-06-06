% ============ DOMAINS ============
course(0..7).
room(0..3).
time_slot(0..5).
teacher(0..4).
dept(sci). dept(hum). dept(eng).
feature(projector). feature(lab).

% ============ COURSE DATA ============
course_teacher(0, 0). course_students(0, 30). course_dept(0, sci).
course_teacher(1, 0). course_students(1, 25). course_dept(1, sci).
course_teacher(2, 1). course_students(2, 40). course_dept(2, sci).
course_teacher(3, 2). course_students(3, 50). course_dept(3, hum).
course_teacher(4, 3). course_students(4, 45). course_dept(4, hum).
course_teacher(5, 4). course_students(5, 60). course_dept(5, eng).
course_teacher(6, 4). course_students(6, 55). course_dept(6, eng).
course_teacher(7, 4). course_students(7, 50). course_dept(7, eng).

% ============ ROOM DATA ============
room_capacity(0, 60). room_feature(0, projector).
room_capacity(1, 50). room_feature(1, projector).
room_capacity(2, 40). room_feature(2, lab). room_feature(2, projector).
room_capacity(3, 30).

% ============ TEACHER AVAILABILITY ============
available(0, 0). available(0, 1). available(0, 2).
available(1, 2). available(1, 3). available(1, 4).
available(2, 0). available(2, 1). available(2, 4). available(2, 5).
available(3, 0). available(3, 2). available(3, 3). available(3, 5).
available(4, 1). available(4, 2). available(4, 3). available(4, 4). available(4, 5).

% ============ ROOM REQUIREMENTS ============
% Chemistry (2) requires lab
requires_feature(2, lab).
% Eng courses (5,6,7) require projector
requires_feature(5, projector).
requires_feature(6, projector).
requires_feature(7, projector).

% ============ PREREQUISITES ============
prereq(0, 1).  % Physics I before Physics II
prereq(5, 6).  % Intro Programming before Data Structures
prereq(6, 7).  % Data Structures before Algorithms

% ============ STUDENT CONFLICTS ============
conflict(1, 4).  % Physics II and Literature
conflict(2, 5).  % Chemistry and Intro Programming

% ============ CHOICE: ASSIGN COURSES ============
{ assigned(C, R, T) : room(R), time_slot(T) } 1 :- course(C).

% ============ HARD CONSTRAINTS ============

% 1. Room Uniqueness: no two courses in same room at same time
:- assigned(C1, R, T), assigned(C2, R, T), C1 < C2.

% 2. Teacher Uniqueness: no two courses by same teacher at same time
:- assigned(C1, R1, T), assigned(C2, R2, T), C1 != C2,
   course_teacher(C1, Te), course_teacher(C2, Te).

% 3. Room Capacity
:- assigned(C, R, T), course_students(C, S), room_capacity(R, Cap), S > Cap.

% 4. Teacher Availability
:- assigned(C, R, T), course_teacher(C, Te), not available(Te, T).

% 5. Room Features
:- assigned(C, R, T), requires_feature(C, F), not room_feature(R, F).

% 6. Prerequisites: prereq course must be in strictly earlier slot
:- assigned(C1, _, T1), assigned(C2, _, T2), prereq(C1, C2), T1 >= T2.

% 7. Student Conflicts: conflicting courses cannot be at same time
:- assigned(C1, _, T), assigned(C2, _, T), conflict(C1, C2).
:- assigned(C1, _, T), assigned(C2, _, T), conflict(C2, C1).

% 8. Global Evening Limit: max 2 courses in slot 5
:- 3 { assigned(C, _, 5) : course(C) }.

% ============ OBJECTIVE: Minimize adjacent same-department pairs ============
% Two courses C1, C2 from same dept in consecutive slots T, T+1
adj_same_dept(C1, C2, T) :- assigned(C1, _, T), assigned(C2, _, T+1),
                              C1 != C2, course_dept(C1, D), course_dept(C2, D),
                              time_slot(T), T < 5.

#minimize { 1, C1, C2, T : adj_same_dept(C1, C2, T) }.

% ============ OUTPUT ============
#show assigned/3.